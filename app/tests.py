from views import statsCollector

TESTING_STATS = """Name                     Remote IP                  Virtual IP      Bytes Received      Bytes Sent      Last Seen
neongm_main_desktop      00.000.000.00:00000        10.6.0.2        211MiB              1.7GiB          Mar 22 2022 - 12:19:22
neongm_android_1         00.000.000.00:00000        10.6.0.3        462MiB              1.6GiB          Mar 21 2022 - 10:36:14
ars_peer_poland          00.000.000.00:00000        10.6.0.4        500MiB              5.1GiB          Mar 19 2022 - 09:28:34
primary                  (none)                     10.6.0.5        0B                  0B              (not yet)
mobile                   (none)                     10.6.0.6        0B                  0B              (not yet)
grig_mobile              00.000.000.00:00000        10.6.0.7        114MiB              2.1GiB          Mar 19 2022 - 10:37:18
neongm_laptop            00.000.000.00:00000        10.6.0.8        37MiB               127MiB          Mar 19 2022 - 10:35:34
grig_desktop             (none)                     10.6.0.9        0B                  0B              (not yet)
: somethin something :"""

st = statsCollector(data=TESTING_STATS)
users = st.get_per_user_stats();

assert st.get_received_traffic() == 1324/1024, f"received traffic calculation failed, true = {1324/1024}, got = {st.get_received_traffic()}"
assert st.get_sent_traffic() ==  1.7+1.6+5.1+2.1+127/1024, f"sent traffic calculation failed, true = {1.7+1.6+5.1+2.1+127/1024}, got = {st.get_received_traffic()}"
assert round(st.get_full_traffic(), 2) == round(1324/1024 + 1.7+1.6+5.1+2.1+127/1024, 2), f"full traffic calculation failed, true = {round(1324/1024 + 1.7+1.6+5.1+2.1+127/1024, 2)}, got = {round(st.get_full_traffic(), 2)}"
assert st.get_peer_count() == 8, f"user count failed, expected {8}, got {st.get_peer_count()}"
assert st.get_active_peer_count() == 5, f"active user count failed, expected {5}, got {st.get_active_peer_count()}"
for user in users: print(f"{user.get_user_name()}\n       virtual ip: {user.get_virtual_ip()}\n       full traffic: {round(user.get_traffic_full(), 2)} GiB\n       sent traffic: {round(user.get_traffic_sent(), 2)} GiB\n       received traffic: {round(user.get_traffic_received(), 2)} GiB\n       active at least once: {user.used_at_least_once()}\n       active recently: {user.is_active()}\n       last seen date: {user.get_last_use_date()}")
