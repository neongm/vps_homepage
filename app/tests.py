from views import statsCollector

TESTING_STATS = """Name                     Remote IP                  Virtual IP      Bytes Received      Bytes Sent      Last Seen
neongm_main_desktop      00.000.000.00:00000        10.6.0.2        211MiB              1.7GiB          Mar 18 2022 - 12:19:22
neongm_android_1         00.000.000.00:00000        10.6.0.3        462MiB              1.6GiB          Mar 19 2022 - 10:36:14
ars_peer_poland          00.000.000.00:00000        10.6.0.4        500MiB              5.1GiB          Mar 19 2022 - 09:28:34
primary                  (none)                     10.6.0.5        0B                  0B              (not yet)
mobile                   (none)                     10.6.0.6        0B                  0B              (not yet)
grig_mobile              00.000.000.00:00000        10.6.0.7        114MiB              2.1GiB          Mar 19 2022 - 10:37:18
neongm_laptop            00.000.000.00:00000        10.6.0.8        37MiB               127MiB          Mar 19 2022 - 10:35:34
grig_desktop             (none)                     10.6.0.9        0B                  0B              (not yet)"""

st = statsCollector()
st.process_data(data=TESTING_STATS)