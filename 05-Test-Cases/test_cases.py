# Source of truth for the SHSS test cases. Generates test_cases.md (repo copy) and the
# per-test markdown bodies pasted into Testomat.
TESTS = [
# ---------------- VERIFICATION SUITE ----------------
dict(suite="Verification", id="TC-V-01", title="TC-V-01 Motion sensor integration", priority="high", type="Functional (integration)",
 reqs="FR-MD-01, FR-MD-02, FR-MD-04, FR-MD-05, PR-01",
 objective="Verify that a Zigbee PIR motion sensor pairs with the CCU, reports motion, tamper and heartbeat events, and that the CCU evaluates motion according to the system mode.",
 pre=["CCU powered, Smart Home Manager running, Zigbee coordinator online",
      "Admin logged in to the web dashboard; system in Disarmed mode",
      "One PIR motion sensor (new, battery inserted) and a stopwatch / event-log timestamp view"],
 steps=[("In the dashboard open Devices → Add device, put the PIR sensor in pairing mode (hold button 5 s).",
         "Sensor appears in the device list within 60 s with status Online and battery level shown."),
        ("Assign the sensor to zone 'Hallway', zone type Instant.",
         "Zone assignment is saved and shown in the device details."),
        ("Walk across the sensor's field of view at 3 m distance while the system is Disarmed.",
         "A 'motion detected – Hallway' event appears in the event log within 1 s; no alarm is raised (Disarmed)."),
        ("Arm the system Away, wait for the exit delay to expire, then walk across the field of view again.",
         "Alarm state entered; indoor siren sounds within 2 s of the motion event; event log shows trigger, zone and timestamp."),
        ("Disarm with the Admin PIN at the keypad.",
         "Siren stops within 1 s; system returns to Disarmed; disarm event logged with user and device."),
        ("Open the sensor housing (tamper switch).",
         "Tamper event 'Hallway PIR – tamper' logged and a health/tamper notification is sent to the Admin."),
        ("Leave the sensor idle and observe the device page for 2 heartbeat intervals (≤ 60 min each, or shortened in test mode).",
         "Heartbeats are received; 'last seen' timestamp updates; sensor stays Online.")],
 expected="The test passes if the sensor pairs, every motion/tamper/heartbeat event is received by the CCU within 1 s, motion is ignored in Disarmed and raises the alarm in Armed Away. It fails if any event is missing, delayed > 1 s, or the alarm is not raised when armed.",
 notes="In test mode the heartbeat interval can be shortened to 1 min so that step 7 does not take two hours. The Zigbee coordinator log gives millisecond timestamps, which is easier than a stopwatch."),

dict(suite="Verification", id="TC-V-02", title="TC-V-02 Door/window sensor integration", priority="high", type="Functional (integration)",
 reqs="FR-DW-01, FR-DW-02, FR-DW-03, FR-DW-05, FR-DW-06",
 objective="Verify that a Zigbee magnetic door/window contact sensor integrates with the CCU and that entry-delay and instant-zone behaviour work as specified.",
 pre=["CCU online; system Disarmed; Admin logged in",
      "Door contact sensor paired and assigned to zone 'Front door' (type Entry, entry delay 30 s)",
      "Window contact sensor paired and assigned to zone 'Living room window' (type Instant)"],
 steps=[("Open the front door while Disarmed.", "'Front door – open' event logged within 1 s; no alarm."),
        ("Close the door; arm the system Away from the app and wait for the exit delay to end.", "System shows Armed Away on app and keypad."),
        ("Open the front door.", "Entry Delay starts: keypad beeps and shows a 30 s countdown; app shows 'Entry delay – Front door'."),
        ("Enter a valid Resident PIN at the keypad within 30 s.", "System disarms; no siren; disarm event logged."),
        ("Arm Away again, wait for exit delay, then open the living-room window (instant zone).", "Alarm raised immediately (siren within 2 s); push notification 'Intrusion – Living room window'."),
        ("Disarm, then leave the window open and request Arm Away from the app.", "App warns 'Living room window is open' and offers Bypass or Cancel; arming is refused unless bypassed."),
        ("Remove the window sensor from its mount.", "Tamper event logged and notification sent.")],
 expected="I treat this as passed when open/close events arrive within 1 s, the entry zone starts the entry delay and disarming within the delay prevents the alarm, the instant zone alarms immediately, open-zone arming is warned/blocked, and tamper is detected. Fail otherwise."),

dict(suite="Verification", id="TC-V-03", title="TC-V-03 Water leak sensor integration", priority="high", type="Functional (integration)",
 reqs="FR-EH-01, FR-EH-03, FR-AL-03",
 objective="Verify that a water leak sensor is treated as a 24-hour zone: it raises a hazard alarm with the water-leak pattern in every mode and can trigger an automation.",
 pre=["CCU online; water leak sensor paired and assigned to zone 'Kitchen – under sink' (24 h zone)",
      "Rule configured: on water leak → switch off smart plug 'Dishwasher'",
      "A shallow dish of tap water; system in Disarmed mode"],
 steps=[("Place the probe tips of the leak sensor in the water.", "Hazard alarm raised within 5 s: indoor siren with the water-leak pattern; app notification 'Water leak – Kitchen'."),
        ("Check the smart plug 'Dishwasher'.", "Plug switched off within 2 s of the alarm; action logged."),
        ("Acknowledge the alarm in the app.", "Siren stops; alarm remains in the log as 'Water leak – acknowledged'."),
        ("Dry the probes.", "Sensor returns to normal; 'Water leak cleared' logged."),
        ("Arm the system Away and repeat step 1.", "Same hazard alarm raised while armed (24 h zone independent of mode)."),
        ("Remove the sensor battery for 2 heartbeat intervals.", "CCU flags sensor Offline and sends a health alert to the Admin.")],
 expected="Pass if water contact raises the hazard alarm within 5 s in Disarmed and Armed modes, the automation runs, and loss of the sensor is reported. Fail if the alarm is late, missing in any mode, or uses the intrusion pattern."),

dict(suite="Verification", id="TC-V-04", title="TC-V-04 Security camera integration", priority="high", type="Functional (integration)",
 reqs="FR-VS-01, FR-VS-02, FR-VS-03, FR-VS-08, PR-04, IR-04",
 objective="Verify that a PoE IP camera is discovered over ONVIF, streams live video to the dashboard and app, records an alarm clip with pre/post-roll, and that stream loss is detected.",
 pre=["PoE switch and CCU online; camera connected to the PoE switch with unique credentials",
      "Admin logged in on the web dashboard and on the mobile app (same LAN)",
      "Hallway PIR sensor paired and linked to the camera's zone; system Disarmed"],
 steps=[("Open Devices → Add camera → Discover.", "Camera is listed via ONVIF with model and IP; adding it completes within 60 s and status shows Online."),
        ("Open Live view for the camera on the dashboard.", "First frame displayed within 3 s; video is continuous with ≤ 1 s latency (clap test)."),
        ("Open Live view on the mobile app (LAN).", "First frame within 3 s; both streams play simultaneously."),
        ("Arm Away, wait for exit delay, then trigger the hallway PIR.", "Alarm raised; recording indicator shows on the camera; snapshot attached to the push notification."),
        ("Disarm and open Recordings → filter by Alarm.", "An alarm clip exists starting ≥ 10 s before and ending ≥ 30 s after the trigger; marked 'alarm' (protected)."),
        ("Export the clip.", "MP4 file downloads and plays."),
        ("Unplug the camera's Ethernet cable.", "Within 30 s the dashboard shows the camera Offline and a health alert is sent to the Admin."),
        ("Reconnect the cable.", "Camera returns Online automatically within 60 s.")],
 expected="Pass if discovery, live view (≤ 3 s first frame), alarm clip with correct pre/post-roll, export and stream-loss detection (≤ 30 s) all work. Fail if any step misses its timing or the clip is missing/unprotected.",
 notes="For the latency check in step 2, clap in front of the camera and count the seconds until the clap shows on screen; it is crude but repeatable."),

dict(suite="Verification", id="TC-V-05", title="TC-V-05 Login functionality – correct credentials", priority="critical", type="Functional (security)",
 reqs="FR-UA-01, FR-UA-02, FR-UA-04, FR-UA-08, FR-UA-09",
 objective="Verify that a valid user can log in to the web dashboard and the mobile app, that MFA is enforced for remote access, and that the login is logged.",
 pre=["Resident account 'resident1' exists with a valid password and TOTP MFA enrolled",
      "Web dashboard reachable on the LAN; mobile app installed on a phone on mobile data (remote path)"],
 steps=[("On the LAN, open the dashboard login page and enter the correct username and password; click Login.", "Login accepted within 2 s; home screen shows the current system mode and the user's name/role (Resident)."),
        ("Check the menu.", "Admin-only items (Users, Configuration) are not visible to the Resident."),
        ("Log out.", "Session ends; browser Back does not show protected pages."),
        ("On the mobile app over mobile data (remote), log in with the same credentials.", "App requests the TOTP code (MFA) because the access is remote."),
        ("Enter the correct 6-digit TOTP code.", "Login completes; dashboard loads; token valid for the session."),
        ("Leave the web session idle for 60 min and then click any action.", "Session has expired; user is returned to the login page."),
        ("As Admin, open the event log.", "Both successful logins are listed with user, device/client and source IP, and the logout and expiry events.")],
 expected="Pass if valid credentials log in within 2 s locally, remote login requires and accepts MFA, role restrictions apply, sessions expire after 1 h idle and all events are logged. Fail if any of these do not occur."),

dict(suite="Verification", id="TC-V-06", title="TC-V-06 Login functionality – wrong credentials and lockout", priority="critical", type="Functional (security)",
 reqs="FR-UA-01, FR-UA-05, FR-UA-09, SR-10",
 objective="Verify that invalid credentials are rejected with a non-specific message, that 5 consecutive failures lock the account for 15 min and notify the Admin, and that failures are logged.",
 pre=["Resident account 'resident1' exists; Admin logged in on a second device to observe notifications",
      "Keypad installed with a Resident PIN configured"],
 steps=[("On the dashboard login page enter the correct username and a wrong password; click Login.", "Login rejected; message 'Invalid username or password' (does not reveal which one is wrong); no session created."),
        ("Enter a non-existent username with any password.", "Same generic message; response time similar to step 1 (no user enumeration)."),
        ("Repeat step 1 until 5 consecutive failures.", "After the 5th failure the account is locked: message states the account is temporarily locked; Admin receives a 'Account locked – resident1' notification."),
        ("Immediately try the correct password.", "Login still refused while the 15 min lock is active."),
        ("At the keypad, enter a wrong PIN 5 times.", "Keypad shows locked state and refuses input for 15 min; Admin notified."),
        ("Enter 5 more wrong PINs after the keypad lock ends (10 total).", "Keypad raises a tamper event; event logged and notification sent."),
        ("After 15 min, log in with the correct password.", "Login succeeds; event log shows all failures, the lockout and the final success with timestamps and source.")],
 expected="Pass if wrong credentials are rejected generically, the 5-failure lockout and Admin notification occur for both password and PIN, the keypad tamper fires at 10 failures, and everything is logged. Fail if login succeeds with wrong credentials, the lock is not applied, or the error reveals account existence.",
 notes="Run this after TC-V-05 so the account is known to be good, and wait out the 15 min lock before any other test that uses resident1."),

dict(suite="Verification", id="TC-V-07", title="TC-V-07 Smart lock controller integration", priority="medium", type="Functional (integration)",
 reqs="FR-DC-01, FR-DC-02, FR-DC-03, FR-DC-04, PR-08",
 objective="Verify that a Zigbee smart door lock pairs with the CCU, executes lock/unlock commands within 1 s, reports its state, and locks automatically on Arm Away.",
 pre=["Smart lock installed on the test door and paired to the CCU; Resident logged in on the app (LAN)",
      "Rule 'Lock front door when Armed Away' enabled"],
 steps=[("Tap Unlock in the app.", "Lock motor runs; state 'Unlocked' shown in the app within 1 s; event logged with user."),
        ("Tap Lock.", "State 'Locked' within 1 s; logged."),
        ("Turn the thumb-turn manually to unlock.", "State change reported to the CCU within 2 s without any command."),
        ("Arm Away from the keypad and wait for the exit delay.", "Lock locks automatically when Armed Away is reached; automation logged."),
        ("Trigger a door contact while armed (simulate intrusion).", "The lock does NOT unlock in response to the sensor event (no automatic unlock on events)."),
        ("Log in as Guest (no lock permission) and try to unlock.", "Command refused with 'Not permitted'; attempt logged.")],
 expected="Pass if commands execute within 1 s, state is reported on manual changes, the auto-lock rule runs on arming, no sensor event unlocks the door and permissions are enforced. Fail otherwise."),

# ---------------- VALIDATION SUITE ----------------
dict(suite="Validation", id="TC-VAL-01", title="TC-VAL-01 Motion detection and alert notification (user acceptance)", priority="critical", type="Non-functional – user acceptance / performance",
 reqs="N1, N2, O2, FR-MD-01, FR-AL-01, FR-NT-01, PR-02, UR-03",
 objective="Validate with a real user that an intrusion into an armed home is detected, the siren sounds and the user receives a useful notification on the phone quickly enough to react.",
 pre=["Reference installation in the test house (CCU, 4 PIR sensors, 2 cameras, indoor and outdoor sirens, keypad)",
      "Homeowner participant with the mobile app installed, logged in, push notifications allowed; phone on mobile data outside the house",
      "System Armed Away; a tester plays the intruder; a stopwatch is started at the moment of entry"],
 steps=[("The 'intruder' enters the living room through an unlocked patio door covered by a PIR sensor.", "Siren sounds within 2 s of entering the sensor's field of view; strobe flashes outside."),
        ("Observe the homeowner's phone.", "Push notification arrives within 5 s showing 'Intrusion – Living room', time, and a camera snapshot; notification sound is distinct from normal alerts."),
        ("Homeowner taps the notification.", "App opens directly on the alarm screen; live view of the living-room camera reachable in ≤ 2 taps and shows the intruder."),
        ("Homeowner chooses 'Silence siren – keep alarm' and then 'Call police' link.", "Siren stops; alarm stays recorded; dialer opens with the configured emergency number (not dialled during test)."),
        ("Ask the participant to rate the experience (1–5) for clarity of the notification and confidence that they could act.", "Rating ≥ 4 for both questions."),
        ("Repeat with the homeowner's dog (≤ 25 kg) walking through the room while armed, no human present.", "No alarm and no notification (pet immunity).")],
 expected="Pass if the siren sounds ≤ 2 s and the notification arrives ≤ 5 s with zone and snapshot, the user reaches live video in ≤ 2 taps, rates the experience ≥ 4/5, and the pet does not cause an alarm. Fail if timings are missed, the notification lacks actionable information, or a false alarm occurs.",
 notes="Agree the intruder's route and timing with the participant beforehand. The point is the participant's reaction to the notification, not surprising them."),

dict(suite="Validation", id="TC-VAL-02", title="TC-VAL-02 Door/window sensor activation (user acceptance)", priority="critical", type="Non-functional – user acceptance",
 reqs="N1, N4, FR-DW-02, FR-DW-03, FR-DW-05, HS-02, HS-05",
 objective="Validate that residents coming home through the front door can disarm within the entry delay without stress, that a window opened while armed raises an immediate alarm, and that the system refuses to arm with an open window unless bypassed.",
 pre=["Reference installation; front door (entry zone, 30 s delay) and 3 window contacts (instant zones)",
      "Two resident participants (one aged 60+) who received the 5-minute introduction; system Armed Away"],
 steps=[("Participant 1 enters through the front door carrying shopping bags.", "Keypad beeps and shows the countdown; participant notices it without prompting."),
        ("Participant 1 enters their PIN at the keypad.", "System disarms before the countdown ends; participant reports no confusion; time from door open to disarm ≤ 20 s."),
        ("Participant 2 (60+) repeats steps 1–2.", "Same outcome; participant can read the keypad from the door position and reach the keys comfortably."),
        ("Arm Away; the tester opens a window from outside.", "Siren within 2 s; both participants receive the notification naming the window."),
        ("Disarm; leave the kitchen window open; participant 2 tries to arm Away from the app.", "App shows a clear warning naming the open window with Bypass / Cancel; participant understands what to do without help."),
        ("Participant 2 closes the window and arms again.", "Arming succeeds; keypad and app show Armed Away.")],
 expected="Pass if both participants disarm within the entry delay at first attempt, the window intrusion alarms immediately with the correct zone, and the open-zone warning is understood and resolved without assistance. Fail if a participant needs help, a false alarm occurs on entry, or the window alarm is late or mislabelled."),

dict(suite="Validation", id="TC-VAL-03", title="TC-VAL-03 Remote camera access and live view (user acceptance)", priority="high", type="Non-functional – user acceptance / performance / security",
 reqs="N2, N5, FR-VS-02, FR-RM-01, FR-RM-02, FR-UA-04, PR-04",
 objective="Validate that a resident away from home can securely open the app, pass MFA, and watch live video from any camera with acceptable start-up time and quality, without any port forwarding on the home router.",
 pre=["Reference installation online; cloud relay connected (dashboard shows 'Cloud: connected')",
      "Participant with the mobile app on mobile data, at least 5 km from the house; MFA enrolled",
      "Router confirmed to have no inbound port-forwarding rules (inspection)"],
 steps=[("Participant opens the app and logs in.", "MFA prompt appears; after the TOTP code the home screen loads within 3 s."),
        ("Participant opens the camera list and taps the back-garden camera.", "Live video starts within 5 s; image is clear enough to recognise a person at 10 m; latency ≤ 2 s (tester waves)."),
        ("Participant switches to a second camera and back.", "Each switch starts within 5 s; no app crash."),
        ("Participant opens Recordings and plays yesterday's alarm clip.", "Clip plays remotely within 5 s."),
        ("Tester on the LAN checks the network monitor on the router.", "Only an outbound TLS connection from the CCU to the cloud relay; no inbound connections; video session is encrypted (WebRTC/SRTP)."),
        ("Ask the participant to rate ease and usefulness (1–5).", "Rating ≥ 4.")],
 expected="The test passes when remote login with MFA, live view (≤ 5 s start, ≤ 2 s latency) and clip playback work over mobile data with only outbound connections from the home, and the user rates it ≥ 4/5. Fail on login failure, start-up > 5 s, visible stalls > 3 s, or any inbound exposure."),

dict(suite="Validation", id="TC-VAL-04", title="TC-VAL-04 System arm/disarm functionality (user acceptance)", priority="critical", type="Non-functional – user acceptance / usability",
 reqs="N4, O4, FR-CC-01, UR-01, UR-02, MS-12, MS-13",
 objective="Validate that residents can arm and disarm the system in all supported ways (app, keypad PIN, NFC tag, schedule) quickly and without errors, and that the current mode is always visible.",
 pre=["Reference installation; 3 participants (Admin, Resident, Guest with time-limited PIN)",
      "Night schedule configured: Armed Night at 23:00, Armed Home at 06:00 (clock may be advanced for the test)"],
 steps=[("Resident arms Away from the app.", "≤ 3 taps and ≤ 10 s; exit delay starts; keypad LED and app show Armed Away after the delay."),
        ("Resident disarms with the NFC tag at the keypad.", "Disarmed within 1 s of the tap; confirmation tone; mode shown on keypad and app."),
        ("Admin arms Home from the keypad (PIN + Home key).", "Armed Home with no exit delay; interior motion sensors shown as bypassed in the app."),
        ("Advance the clock to 23:00.", "System switches automatically to Armed Night; all users notified; event logged with cause 'schedule'."),
        ("Guest enters the time-limited PIN during its validity window.", "Disarm succeeds; event logged as the Guest."),
        ("Guest enters the same PIN after the window has expired.", "Disarm refused; Admin notified."),
        ("Each participant fills in the SUS questionnaire for arm/disarm.", "Average SUS ≥ 75; all participants succeeded at the first attempt.")],
 expected="Pass if all arm/disarm methods work at first attempt within the time limits, the schedule transition occurs, expired guest access is refused, every transition is logged, and SUS ≥ 75. Fail if any participant fails a method, the mode display is inconsistent between keypad and app, or SUS < 75."),

dict(suite="Validation", id="TC-VAL-05", title="TC-VAL-05 Simultaneous sensor triggers (load test)", priority="high", type="Non-functional – performance / load",
 reqs="PR-01, PR-02, PR-03, RL-05, FR-AL-01",
 objective="Validate that when three or more sensors are triggered at the same time the system raises a single coherent alarm, loses no events, and still meets the siren and notification latency targets.",
 pre=["Reference installation Armed Away with ≥ 6 sensors online (3 PIR, 2 door/window, 1 glass-break)",
      "Three testers positioned at different sensors with synchronised countdown; event log with millisecond timestamps; a load script able to inject 20 simulated Zigbee events/second (test mode) is available",
      "Two users logged in on phones to receive notifications"],
 steps=[("On the count of zero, three testers trigger a PIR, a door contact and a window contact within the same second.", "All three events appear in the log with timestamps within 1 s of the trigger."),
        ("Observe the sirens and phones.", "One alarm raised (not three separate alarms); siren within 2 s of the first event; one consolidated notification listing all three zones within 5 s."),
        ("Repeat with 5 sensors triggered simultaneously.", "Same behaviour; no event lost; latencies unchanged."),
        ("Run the load script injecting 20 events/s for 60 s while the system is armed and trigger a real sensor at second 30.", "The real trigger raises the alarm within 2 s; CPU on the CCU < 80 %; no dropped events (script count = log count)."),
        ("Disarm and open the event log.", "Every event from steps 1–4 is present with the correct zone and order; cameras of all triggered zones have alarm clips.")],
 expected="Passed when simultaneous and high-rate triggers produce no lost events, a single alarm with all zones, and siren ≤ 2 s / notification ≤ 5 s in every run. Fail if any event is missing, multiple separate alarms are raised, or latency exceeds the limits.",
 notes="The load script injects events through the coordinator's test interface; never run it against a system that is in real use."),

dict(suite="Validation", id="TC-VAL-06", title="TC-VAL-06 High-volume user access (load test)", priority="high", type="Non-functional – performance / load",
 reqs="PR-06, PR-04, FR-CC-07, SR-10",
 objective="Validate that three or more devices can use the app and dashboard at the same time (live video, arm/disarm, log browsing) while the system keeps responding within the required times and alarm processing is unaffected.",
 pre=["Reference installation; 5 client devices: 3 phones (app, 2 on LAN, 1 remote), 1 laptop (web dashboard), 1 wall keypad",
      "Timing captured with a screen recorder per device; system Disarmed at start"],
 steps=[("All three phones open live view of different cameras at the same time.", "Each stream starts ≤ 3 s (LAN) / ≤ 5 s (remote) and plays without stalls > 1 s for 2 min."),
        ("While streams run, the laptop browses the event log and exports 1 month as CSV, and the keypad user arms the system Home.", "Log pages load ≤ 2 s; export completes; arming takes effect within 1 s and is reflected on all 4 screens within 1 s."),
        ("Phone 1 (Resident) and phone 2 (Admin) tap Disarm at the same moment.", "System disarms once; both apps show Disarmed; log shows one disarm with the first user and the second request as 'already disarmed'."),
        ("With all sessions active, trigger a water-leak sensor.", "Hazard alarm and notifications to all 3 phones within 5 s; no slowdown in the streams."),
        ("Increase to 10 concurrent sessions using the load tool (API clients polling status every second).", "95th-percentile API response ≤ 1 s local; CCU remains responsive; no client errors."),
        ("Run a burst of 100 requests/s against the local API for 30 s from one client.", "Requests are rate-limited (HTTP 429) but alarm processing and the other clients continue normally.")],
 expected="Pass if ≥ 3 devices operate concurrently with live video, control and log access within the specified response times, conflicting commands are handled safely, alarms are not delayed, and the API degrades gracefully under overload. Fail if any client sees > 2 s responses, a stream stalls, or an alarm is delayed.",
 notes="Screen-record each phone so the timings can be read back frame by frame instead of relying on a stopwatch."),

dict(suite="Validation", id="TC-VAL-07", title="TC-VAL-07 Internet outage resilience (user need N3)", priority="high", type="Non-functional – reliability / availability",
 reqs="N3, FR-CC-04, FR-CC-09, FR-NT-04, FR-RM-04, RL-06",
 objective="Validate that the home remains protected and the user is still alerted when the internet connection fails, and that remote clients are informed honestly.",
 pre=["Reference installation Armed Away; LTE backup modem with active SIM; one phone on the LAN, one remote",
      "Admin can disconnect the router's WAN cable"],
 steps=[("Disconnect the WAN cable.", "Within 60 s the keypad/app (LAN) show 'Internet offline – LTE backup'; Admin receives a health alert via LTE."),
        ("Remote phone opens the app.", "App shows 'System offline from cloud since <time>' instead of stale data."),
        ("Trigger a PIR sensor.", "Siren within 2 s; notification arrives on both phones within 15 s (via LTE); event logged."),
        ("Disarm at the keypad; arm again from the LAN app; view a camera live on the LAN app.", "All local functions work normally."),
        ("Reconnect the WAN cable.", "Cloud connection restored within 60 s; remote app shows live data again; any queued cloud backups complete.")],
 expected="Pass if detection, siren, local control and local video are unaffected, notifications arrive ≤ 15 s over LTE, and the outage/restoration is reported. Fail if any local function depends on the internet or notifications are lost."),

dict(suite="Validation", id="TC-VAL-08", title="TC-VAL-08 Mains power failure and backup operation", priority="high", type="Non-functional – reliability",
 reqs="PR-12, PR-14, RL-07, FR-CC-09",
 objective="Validate that the system keeps protecting the home on battery backup for at least 4 hours and recovers automatically when power returns.",
 pre=["Reference installation on UPS with fully charged battery; system Armed Away; cameras on the UPS-backed PoE switch"],
 steps=[("Switch off the mains breaker feeding the CCU, router and PoE switch.", "No interruption: system stays Armed Away; health alert 'Mains power lost – on battery' within 60 s."),
        ("Trigger a door contact after 10 min on battery.", "Siren and notifications work normally."),
        ("Leave the system on battery and check every 30 min.", "System, cameras and keypad remain operational for ≥ 4 h; battery percentage visible in the app."),
        ("Restore mains after 4 h.", "'Mains power restored' alert; UPS charging; no mode change."),
        ("Simulate a full power loss (remove UPS output for 1 min) and restore.", "CCU boots and is armed-capable within 90 s, restoring the previous mode (Armed Away) automatically.")],
 expected="Passed when the system runs ≥ 4 h on backup without loss of protection, reports the outage and restoration, and auto-recovers the previous mode within 90 s after a cold start. Fail otherwise."),

dict(suite="Validation", id="TC-VAL-09", title="TC-VAL-09 Guest first-use disarm (usability)", priority="medium", type="Non-functional – usability",
 reqs="UR-04, FR-UA-07, FR-UA-06",
 objective="Validate that an untrained guest given only a PIN and a one-line instruction can disarm the system within the entry delay at the first attempt, and that the guest's access is limited as intended.",
 pre=["Reference installation Armed Away; Admin has created a Guest with a PIN valid today 09:00–12:00 and permissions: disarm, lights",
      "5 guest participants who have never seen the system; each receives only: 'Enter 4821 on the keypad by the door'"],
 steps=[("Each guest enters through the front door and uses the keypad.", "≥ 90 % (at least 5 of 5 or 9 of 10) disarm successfully at the first attempt within the 30 s entry delay."),
        ("Guest opens the app invitation on their phone and tries to open the camera list.", "Cameras are not available to the Guest role; lights are controllable."),
        ("At 12:01 a guest tries the PIN again.", "Refused; Admin notified of an expired-code attempt."),
        ("Ask guests to rate how clear the keypad feedback was (1–5).", "Average ≥ 4.")],
 expected="Pass if ≥ 90 % of untrained guests disarm at first attempt, guest permissions are enforced and the expired code is refused. Fail if the success rate is below 90 % or a guest can access functions outside the granted permissions."),
]

PRIORITY_LABEL = {"critical": "Critical", "high": "High", "medium": "Medium", "low": "Low"}

def body(t):
    L = []
    L.append("### Description")
    L.append(f"**Objective:** {t['objective']}")
    L.append("")
    L.append(f"**Priority:** {PRIORITY_LABEL[t['priority']]}")
    L.append(f"**Type:** {t['type']}")
    L.append(f"**Requirements covered (SysRS):** {t['reqs']}")
    L.append("")
    L.append("### Prerequisite (Precondition)")
    for p in t["pre"]:
        L.append(f"* {p}")
    L.append("")
    L.append("### Steps")
    for i, (s, e) in enumerate(t["steps"], 1):
        L.append(f"{i}. {s}")
        L.append(f"*Expected:* {e}")
        L.append("")
    L.append("### Expected result")
    L.append(t["expected"])
    if t.get("notes"):
        L.append("")
        L.append(f"**Notes:** {t['notes']}")
    return "\n".join(L)

if __name__ == "__main__":
    import json, pathlib
    out = ["# SHSS Test Cases: Verification and Validation", "",
           "Source for the Testomat project *Smart Home System*. Each test uses the format: name, objective, priority, type, precondition, steps with expected outcome per step, expected result. Requirement IDs refer to the SysRS.", ""]
    for suite in ("Verification", "Validation"):
        out.append(f"## Suite: {suite}"); out.append("")
        for t in TESTS:
            if t["suite"] != suite: continue
            out.append(f"## {t['title']}"); out.append(""); out.append(body(t)); out.append(""); out.append("---"); out.append("")
    pathlib.Path("test_cases.md").write_text("\n".join(out))
    pathlib.Path("/tmp/claude-1000/-home-ag7-Downloads/9a9e0d98-4dca-4eed-bcd2-b442256f3aac/scratchpad/tests.json").write_text(
        json.dumps([dict(suite=t["suite"], title=t["title"], priority=t["priority"], body=body(t)) for t in TESTS], indent=1))
    print(len(TESTS), "tests;", sum(1 for t in TESTS if t["suite"]=="Verification"), "verification,", sum(1 for t in TESTS if t["suite"]=="Validation"), "validation")
