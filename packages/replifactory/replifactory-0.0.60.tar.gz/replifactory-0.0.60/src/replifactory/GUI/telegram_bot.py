from telegram.ext import Updater, CommandHandler, Filters
import subprocess
from replifactory.util import read_csv_tail
import time
import os
import numpy as np
import matplotlib.pyplot as plt


bot = None


class TelegramBot:
    def __init__(self, TOKEN, IDs, exp_dir):
        self.exp_dir = exp_dir
        self.updater = Updater(TOKEN, use_context=True)
        # Get the dispatcher to register handlers
        dp = self.updater.dispatcher
        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("plot", self.plot, filters=Filters.user(user_id=list(IDs))))
        dp.add_handler(CommandHandler("photo", photo, filters=Filters.user(user_id=list(IDs))))
        dp.add_handler(CommandHandler("getpublicip", getpublicip, filters=Filters.user(user_id=list(IDs))))
        dp.add_handler(CommandHandler("getotherips", getotherips, filters=Filters.user(user_id=list(IDs))))
        dp.add_handler(CommandHandler("cmd", cmd, filters=Filters.user(user_id=list(IDs))))
        dp.add_handler(CommandHandler("list_dilutions", self.list_dilutions, filters=Filters.user(user_id=list(IDs))))

    def start(self):
        global bot
        if bot is not None:
            try:
                bot.stop()
            except:
                pass
        bot = self
        if bot.updater.running:
            print("stopping")
            self.stop()
        self.updater.start_polling()
        print("started bot")

    def stop(self):
        self.updater.stop()

    def list_dilutions(self, update, context):
        reply = ''
        for vial_num in range(1, 8):
            reply += 'Vial' + str(vial_num) + ':\n'
            path_vial = self.exp_dir + 'vial_' + str(vial_num) + '/log2_dilution_coefficient.csv'
            if os.path.exists(path_vial):
                with open(path_vial, 'r') as file:
                    lines = file.readlines()[1:]
                    for i in range(len(lines) - 3, len(lines)):
                        reply += str(i + 1) + ': ' + ' '.join(
                            time.ctime(round(float(lines[i].split()[0][:-1])) + 7 * 3600).split()[
                            1:4]) + '\n'  # TODO local time on raspberry needs adding 7 hours
                    reply += '\n'
        update.message.reply_text(reply)

    def plot(self, update, context):
        text = "Here's the plot"
        update.message.reply_text(text)
        self.make_plot()
        plot_dir = os.path.join(self.exp_dir, "telegram_plot.png")
        update.message.reply_document(open(plot_dir, "rb"))
        # print(update)

    def make_plot(self):
        exp_dir = self.exp_dir
        fig, ax = plt.subplots(figsize=[12, 6], dpi=100)
        fig.patch.set_facecolor('w')
        ax3 = fig.axes[0].twinx()
        ax4 = ax.twinx()
        colors = {1: 'tab:blue',
                  2: 'tab:orange',
                  3: 'tab:green',
                  4: 'tab:red',
                  5: 'tab:purple',
                  6: 'tab:brown',
                  7: 'tab:pink'}

        vials_list = [1, 2, 3, 4, 5, 6, 7]
        last_hours = 24
        for v in vials_list:
            directory = os.path.join(exp_dir, "vial_%d" % v)
            od_filepath = os.path.join(directory, "od.csv")
            df = read_csv_tail(filepath=od_filepath, lines=last_hours * 60)
            t = df.index.values
            od = df.values.ravel()
            t_min = t[-1] - last_hours * 3600
            odw = od[t > t_min]
            tw = t[t > t_min]
            drug_concentration_file = os.path.join(directory, "medium2_concentration.csv")
            tdose = None
            dosevalues = None
            if os.path.exists(drug_concentration_file):
                dosedf = read_csv_tail(drug_concentration_file, lines=50 + last_hours * 10)
                tdose = dosedf.index.values
                dosevalues = dosedf.values.ravel()[tdose > t_min]
                tdose = tdose[tdose > t_min]

            if tdose is not None:
                if len(tdose) > 0:
                    ax3.step(tdose / 3600, dosevalues, "^-.", color=colors[v], alpha=0.6, label="Vial %d dose" % v,
                             where="post")

            # plot growth rate
            od_values = odw
            time_values = tw
            dilution_timepoints = tdose
            od = np.array(od_values)
            t = np.array(time_values)

            # i = 0
            # lines = []
            if len(od) > 0:
                ax.plot(t / 3600, od, ".:", color=colors[v], markersize=3, label="Vial %d OD" % v)

                # if now-t[-1]<3600*24:
                #     ax.axvline(now,linestyle="-",linewidth=1,color="pink",label="now (%s)"%time.ctime()[4:-5])
                # ax.set_ylim(-0.05, 1.6)

                od[od <= 0] = 1e-6
                ax.set_ylabel("Optical Density")
                ax.set_xlabel("Time [hours]")

            gen_file = os.path.join(directory, "log2_dilution_coefficient.csv")

            if os.path.exists(gen_file):
                df = read_csv_tail(gen_file, lines=last_hours * 60)  # 24h
                df = df[df.index > t_min]
                if df.shape[0] > 0:
                    df.index = df.index / 3600
                    df.log2_dilution_coefficient.plot(style="--", marker="s", color=colors[v], alpha=0.3,
                                                      label="Vial %d generation" % v, axes=ax4)

            handles, labels = [], []
            for axis in fig.axes:
                handle, label = axis.get_legend_handles_labels()
                axis.legend([])
                handles += handle
                labels += label
            ax.legend(handles, labels, loc=2)

            xticks = ax.get_xticks()
            for axis in fig.axes:
                axis.set_xticks(xticks)

            tmin = xticks[0]
            xtick_labels = [round(t - tmin, 2) for t in xticks]
            # fig.axes[1].set_ylim(0.1, 10)
            ax.set_xticklabels(xtick_labels)
            # fig.axes[1].set_yticks([])

            ax.set_yscale("log")
            od_ticks = [0.001, 0.01, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 1]
            ax.set_yticks(od_ticks)
            ax.set_yticklabels(od_ticks)
            ax.set_ylim(0.0008, 1.6)
            ax.grid(color="k", linestyle="--", alpha=0.3)
            ax.set_xlabel("Time [hours from %s]" % time.ctime(tmin * 3600))
        ax3.spines["left"].set_position(("axes", -0.08))
        ax3.yaxis.set_label_position("left")
        ax3.yaxis.set_ticks_position("left")
        ax3.yaxis.set_tick_params(color="r")
        ax3.set_ylabel("Dose [mM]", color="r")
        ax3.grid(color="r", linestyle=":", alpha=0.5)

        ax4.yaxis.set_tick_params(color="g")
        ax4.spines["right"].set_position(("axes", 1))
        ax4.grid(color="g", linestyle="-.", alpha=0.5)
        ax4.set_ylabel("Generation number", color="g")

        plot_title = os.path.abspath(exp_dir)
        fig.axes[0].set_title(plot_title)
        #     plt.show()
        plt.savefig(os.path.join(exp_dir, "telegram_plot.png"), dpi=200)
        plt.close()

# Usage:
# bot = TelegramBot(TOKEN, IDs)
# bot.start()




def getpublicip(update, context):
    publicip = os.popen("curl icanhazip.com").read().rstrip()
    update.message.reply_text(publicip)


def getotherips(update, context):
    otherips = os.popen("hostname -I").read().rstrip()
    update.message.reply_text(otherips)


def cmd(update, context):
    cmd = " ".join(context.args)
    reply = command_timeout(command=cmd, timeout=20)
    update.message.reply_text(reply)


def command_timeout(command, timeout):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for t in range(timeout):
        time.sleep(1)
        if p.poll() is not None:
            reply = "\n".join(x.decode() for x in p.communicate())
            return reply
            break
    p.kill()
    return "process killed after %d seconds" % timeout


def photo(update, context):
    text = "Here's the photo"
    update.message.reply_text(text)
    os.system("raspistill -o telegram_photo.png")
    plot_dir = os.path.join("telegram_photo.png")
    update.message.reply_document(open(plot_dir, "rb"))
    # print(update)


