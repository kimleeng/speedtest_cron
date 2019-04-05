import traceback
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
import speedtest


def main():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("speedtest").sheet1

    try:
        s = speedtest.Speedtest()
        s.get_best_server()
        s.download()
        s.upload()
        results_dict = s.results.dict()
        # Sample output
        # {'download': 776625654.5262586, 'upload': 735739251.0368077, 'ping': 1.919, 'server':{'url': 'http://speedtest.zensystems.dk:8080/speedtest/upload.php', 'lat': '55.6750', 'lon': '12.5687', 'name': 'Copenhagen', 'country': 'Denmark', 'cc': 'DK', 'sponsor': 'Zen Systems', 'id': '1133', 'url2': 'http://speedtest2.zensystems.dk/speedtest/upload.php', 'host': 'speedtest.zensystems.dk:8080', 'd': 0.7333373232273797, 'latency': 1.919},'timestamp': '2019-04-05T09:32:33.725538Z', 'bytes_sent': 151519232, 'bytes_received': 409373932, 'share': None,'client': {'ip': '193.3.234.5', 'lat': '55.6786', 'lon': '12.5589', 'isp': 'TDC Danmark', 'isprating': '3.7', 'rating': '0', 'ispdlavg': '0', 'ispulavg': '0', 'loggedin': '0', 'country': 'DK'}}
        row = [results_dict["timestamp"], results_dict["download"], results_dict["upload"], results_dict["ping"], results_dict["client"]["ip"]]
        sheet.insert_row(row, 1)
    except Exception as e:
        row = []
        sheet.insert_row(row, 1)
        print(str(traceback.format_exc()))


if __name__ == "__main__":
    main()
