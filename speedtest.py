import os
import re
import subprocess
import time
import traceback


def main(argv):
    print("Starting")

    parser = argparse.ArgumentParser(description='Run speedtest and log, meant for cron')
    parser.add_argument("-o", "--output_file",
                        type=str,
                        required=True
                        default="speedtest_log.csv")
    args = parser.parse_args()

    ping = ""
    download = ""
    upload = ""

    try:
        response = subprocess.Popen('speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()
        ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)[0].replace(",", ".")
        download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)[0].replace(",", ".")
        upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)[0].replace(",", ".")
    except Exception as e:
        sys.stderr.write(str(traceback.format_exc()))

    try:
        with open(args.output_file, "a+") as log_file:
            if os.stat('/home/pi/speedtest/speedtest.csv').st_size == 0:
                log_file.write('Date,Time,Ping (ms),Download (Mbit/s),Upload (Mbit/s)\n')
            log_file.write("{},{},{},{},{}\n".format(time.strftime('%d/%m/%y'), time.strftime('%H:%M'), ping, download, upload))
    except Exception as e:
        sys.stderr.write(str(traceback.format_exc()))

if __name__ == "__main__":
    main(sys.argv)