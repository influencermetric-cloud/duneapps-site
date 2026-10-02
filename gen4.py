#!/usr/bin/env python3
"""The ToDo product page and its privacy policy.

Apple rejects a version whose support or privacy link does not resolve, and the App Store
listing points both at https://duneapps.com/todo/ and /todo/privacy/. Neither existed
until this file did.

Every claim below was read out of the shipping code on 2 Oct 2026, not from the spec:
  * ToDo Pro, $29.99 once, family    -> tools/setup-iap.py, Shared/Logic/Pro.swift
  * home AND lock-screen widgets     -> Widgets/ToDoPlannerWidgets.swift (accessory* families)
  * Siri / shortcuts                 -> ToDoPlanner/App/AppShortcuts.swift, Shared/Intents/
  * share sheet                      -> ShareExtension/ShareViewController.swift
  * Reminders, Todoist, TickTick     -> Shared/Import/Importers.swift
  * backup and restore               -> Shared/Import/Backup.swift
  * undo on finish/delete/reschedule -> design/SPEC.md, implemented app-wide

iCloud sync is written but switched OFF (the container does not exist yet), so this page
must not mention it as a feature. It is listed under what the app does not do.

Run: python3 gen4.py   (or build_all.py, which calls it)
"""

import json

from build import render
from gen2 import FAQ_CSS, PAGE_CSS, faq_block, faq_ld

APP_ID = "6818510042"
STORE = f"https://apps.apple.com/app/id{APP_ID}"

# Flip to True the day Apple approves it; the hero and the closing panel both read this.
LIVE = False

CTA = (f'<a class="btn btn-primary" href="{STORE}" data-app="todo" data-place="hero">Get ToDo — free</a>'
       if LIVE else
       '<span class="btn btn-primary is-soon" aria-disabled="true">Coming to the App Store</span>')

FAQ = [
    ("What is free and what costs money?",
     "The list is free forever — unlimited tasks, lists, dates, repeats, widgets, Siri, the share "
     "sheet, imports and backup. Not a trial and not capped. ToDo Pro is $29.99 once and adds the "
     "four quick ways to get things in: talking instead of typing, pulling tasks off a photo, "
     "Plan my day, and breaking a big task into steps. One payment, Family Sharing on, and no "
     "subscription ever."),
    ("Do I need an account?",
     "No. There is no sign-up, no email, no password and no “continue with Apple”. You open the "
     "app and start typing. That also means nobody can lock you out of your own list."),
    ("Where are my tasks stored?",
     "On your iPhone, in the app's own storage. ToDo makes no network connections, so there is no "
     "server holding a copy. The App Store privacy label reads Data Not Collected."),
    ("What happens if I lose my phone?",
     "Your tasks go with it, which is the honest trade for having no servers. Export a backup file "
     "from Settings and keep it somewhere you control — restoring it on a new phone brings "
     "everything back. Your iPhone's own iCloud backup also includes the app's data."),
    ("Can I bring my tasks over from another app?",
     "Yes, from Apple Reminders, Todoist and TickTick. Lists, due dates and completion state come "
     "across. There is no importer for anything else yet."),
    ("What does the quick add actually understand?",
     "Dates, times and repeats written the way you would say them. “Friday 2pm”, “tomorrow”, "
     "“in 3 days”, “every Monday 6pm”, “daily”. The parsed parts appear as chips while you type "
     "and each one is tappable, so a wrong guess costs one tap to fix."),
]

BODY = f'''<section class="hero"><div class="wrap split">
  <div>
    <span class="badge">New · <b>iPhone</b></span>
    <h1>A list that doesn't want your email address.</h1>
    <p class="lede">Type a sentence. It becomes a task with the date, the time and the repeat
      already on it. No account, no subscription, nothing uploaded — and in version 1.0 there is
      nothing to buy at all.</p>
    <div class="actions">
      {CTA}
      <a class="btn btn-dark" href="#free">What is free, and what is not</a>
    </div>
    <div class="assurances"><span>No account</span><span>No subscription</span><span>Free list, forever</span></div>
  </div>
  <div class="visual"><div class="bubble"></div><div class="phones">
    <img src="/assets/todo-2.png" alt="Typing a task and watching the date become a chip" loading="lazy">
    <img src="/assets/todo-1.png" alt="The ToDo Today screen" loading="lazy">
    <img src="/assets/todo-3.png" alt="Planning the day" loading="lazy">
  </div></div>
</div></section>

<section class="section" id="free"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">The part worth reading</span>
    <h2>Free list. One payment for the clever bits.</h2>
    <p>Every other app on this shelf is free until it isn't, then bills you every year for ever.
      Here the list is free with no cap and no trial clock, and the things that make it fast are
      a single $29.99 payment that covers your whole family. Less than one year of any
      subscription in this category, and then nothing, for good.</p></div>
  <table class="cmp reveal">
    <thead><tr><th>&nbsp;</th><th style="color:var(--teal)">ToDo</th><th>What usually happens</th></tr></thead>
    <tbody>
      <tr><td>Account required</td><td class="ours">No</td><td class="them">Email and password before you can type</td></tr>
      <tr><td>The list itself</td><td class="ours">Free, uncapped, forever</td><td class="them">Free until a limit, then a subscription</td></tr>
      <tr><td>How you pay</td><td class="ours">$29.99 once</td><td class="them">Every year, for as long as you use it</td></tr>
      <tr><td>Your family</td><td class="ours">Family Sharing, up to 6 people</td><td class="them">Priced per person</td></tr>
      <tr><td>Where your tasks live</td><td class="ours">Your iPhone only</td><td class="them">Their servers</td></tr>
      <tr><td>Undo after deleting</td><td class="ours">Yes, on everything</td><td class="them">Often nothing</td></tr>
    </tbody>
  </table>
  <p class="note">The "usually" column describes the pricing model of the best-selling to-do apps
    on the App Store, which are free downloads with a subscription behind them, and the complaints
    that fill their one-star reviews. Prices change; check theirs before you believe ours. ToDo
    shows your own currency at checkout, not dollars.</p>
</div></section>

<section class="section" style="background:var(--bg-2)"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">What it does</span><h2>Three screens, nothing to learn</h2></div>
  <div class="grid g-2" style="margin-top:40px">
    <div class="card reveal"><h3>Type it the way you'd say it</h3>
      <p>"Call the dentist Friday 2pm" arrives as a task dated Friday at two. "Bins out every
        Tuesday" repeats itself. The parts it recognises turn into chips as you type, and every
        chip is tappable, so correcting a wrong guess costs one tap rather than a trip into a
        settings screen.</p></div>
    <div class="card reveal"><h3>Tasks, Calendar, Progress</h3>
      <p>That is the whole structure. Tasks puts overdue, today, tomorrow and upcoming in one list
        and filters by a tap on any of your lists. Calendar shows the month. Progress shows what
        you finished this week and what the next seven days hold. No projects, no boards, no
        priority matrix to configure.</p></div>
    <div class="card reveal"><h3>Swipe to finish, swipe to move</h3>
      <p>Right to complete, left to push it to another day. Both show a toast with Undo for six
        seconds. Deleting a list without warning is the single loudest complaint in this category's
        reviews, so nothing here is destructive without a way back.</p></div>
    <div class="card reveal"><h3>On the home screen and the lock screen</h3>
      <p>Widgets in three home-screen sizes and three lock-screen ones, showing what is next. They
        redraw when the list changes rather than whenever iOS feels like it — the other common
        one-star review.</p></div>
    <div class="card reveal"><h3>Add it without opening the app</h3>
      <p>Ask Siri, or send text to ToDo from the share sheet in any other app. Both run the same
        parser, so a shared sentence keeps its date.</p></div>
    <div class="card reveal"><h3>Say it, or photograph it</h3>
      <p>Hold the microphone and talk; the speech becomes text on your iPhone. Or photograph a
        handwritten note, a notice or a whiteboard and ToDo pulls the tasks out of the picture.
        Both run on the device.</p></div>
    <div class="card reveal"><h3>Plan my day</h3>
      <p>It reads the gaps between today's calendar events and lays your unscheduled tasks into
        them, with a suggested length for each. Change any of it, then apply the lot in one tap.</p></div>
    <div class="card reveal"><h3>See the week honestly</h3>
      <p>Progress counts what you actually finished per day, what is still pending and what is
        coming in the next seven days, broken down by list. No streaks and no guilt mechanics.</p></div>
    <div class="card reveal"><h3>Bring your old list with you</h3>
      <p>Import from Apple Reminders, Todoist or TickTick, with lists, due dates and completion
        intact. Export a backup file whenever you like and restore it on a new phone.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">Being straight about it</span><h2>What ToDo does not do</h2></div>
  <div class="grid g-2" style="margin-top:40px">
    <div class="card reveal"><h3>No sync between devices, yet</h3>
      <p>Tasks live on the phone that made them. The sync is written but switched off until the
        iCloud side is set up properly, and shipping a sync that silently does nothing is worse
        than not offering one. Backup and restore is the bridge in the meantime.</p></div>
    <div class="card reveal"><h3>No iPad or Mac app</h3>
      <p>iPhone only. There is no web version and no Android version. If you need your list on a
        laptop during the day, this is not the product yet.</p></div>
    <div class="card reveal"><h3>No projects, boards or collaboration</h3>
      <p>No sub-projects, no Kanban, no assigning a task to someone else, no shared lists. It is a
        personal list. If you are running a team, you want something else and no amount of privacy
        makes up for it.</p></div>
    <div class="card reveal"><h3>It does not write to your calendar</h3>
      <p>Plan my day can read your calendar, with your permission, to find the gaps between your
        events. It never writes to it, never copies an event and never uploads one — your tasks
        do not appear in Calendar, and your meetings do not appear in ToDo.</p></div>
  </div>
</div></section>

{faq_block(FAQ)}

<section class="section" id="support"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">Support</span><h2>Something wrong? Say so.</h2>
    <p>Email <a href="mailto:nahidsaleem1@gmail.com">nahidsaleem1@gmail.com</a> with your iOS
      version and what happened, and it gets read by the person who wrote the app. There is no
      support queue and no bot in front of it.</p>
    <p style="margin-top:16px"><a href="/todo/privacy/">Privacy policy</a></p></div>
</div></section>

<section class="section"><div class="wrap"><div class="final reveal">
  <h2>Write it down.<br>That's the whole app.</h2>
  <div class="actions">
    {CTA}
    <a class="btn btn-dark" href="/">More from Dune Apps</a></div>
  <div class="assurances" style="justify-content:center"><span>Free</span><span>No account</span><span>iOS 17 or later</span></div>
</div></div></section>'''

PRIVACY_CSS = """
  .legal { max-width: 68ch; margin: 0 auto; padding: 64px 0 90px; }
  .legal h1 { font-size: clamp(2rem, 4vw, 2.9rem); margin-bottom: 10px; }
  .legal .when { color: var(--faint); font-size: .92rem; }
  .legal h2 { font-size: 1.32rem; margin: 46px 0 12px; }
  .legal p, .legal li { color: var(--muted); line-height: 1.75; }
  .legal ul { margin: 14px 0 0 20px; }
  .legal li { margin-bottom: 8px; }
  .legal .lead { font-size: 1.14rem; color: var(--text); font-weight: 500; }
"""

PRIVACY = '''<section class="wrap"><div class="legal">
  <h1>ToDo privacy policy</h1>
  <p class="when">Last updated 2 October 2026</p>

  <p class="lead" style="margin-top:28px">ToDo does not collect, transmit or share any data. It has
    no accounts, no analytics, no advertising identifiers and no servers, and the app makes no
    network connections of any kind.</p>

  <h2>Where your tasks live</h2>
  <p>Your tasks, lists, notes, subtasks and completion history are stored in the app's own private
    storage on your iPhone. Nothing is sent anywhere to create them and nothing is sent anywhere
    afterwards. Deleting the app deletes this data.</p>

  <h2>What we can see</h2>
  <p>Nothing. There is no server to receive it, so no copy of your list exists anywhere but on your
    own device. That is also why we cannot recover it if you lose the phone — export a backup
    file from Settings and keep it somewhere you control.</p>

  <h2>Notifications</h2>
  <p>Reminders are scheduled by iOS on your device. They are not push notifications, nothing is sent
    from a server, and the text of a task never leaves the phone.</p>

  <h2>Siri and the share sheet</h2>
  <p>Adding a task by voice uses Apple's own speech recognition, which is governed by your iPhone's
    Siri settings and Apple's privacy policy, not ours. Text sent to ToDo from another app's share
    sheet is handed over by iOS and stored like anything else you type. We receive neither.</p>

  <h2>Importing from other apps</h2>
  <p>Importing from Apple Reminders asks your permission and reads only your reminders, on the
    device. Importing from Todoist or TickTick reads a file you export from them and hand to ToDo.
    In both cases the data is copied locally. ToDo never contacts those services.</p>

  <h2>Your calendar</h2>
  <p>Plan my day asks permission to read the events on your iPhone so it can find the free time
    between them. It reads titles and times only, on the device, to lay out the suggestion you see.
    Nothing about your calendar is stored in ToDo, copied, or sent anywhere, and ToDo never writes
    an event. Refuse the permission and Plan my day still works — it just spaces tasks evenly
    instead of around your meetings.</p>

  <h2>The microphone</h2>
  <p>ToDo listens only while you hold the microphone button. The audio is turned into text by
    Apple's speech recognition, which your iPhone's Siri settings govern, and the recording is not
    kept. We never receive the audio or the text.</p>

  <h2>The camera and photos</h2>
  <p>Photographing a note reads the text out of that one image on the device, to make tasks from
    it. The photo is not saved by ToDo and not uploaded. If you attach a photo to a task instead,
    ToDo receives only the images you pick through Apple's photo picker and has no access to the
    rest of your library.</p>

  <h2>Backups</h2>
  <p>The backup file ToDo exports goes wherever you choose to put it and is yours to look after.
    Separately, your iPhone's own iCloud or computer backup may include this app's data; that
    backup is governed by your Apple Account settings, not by ToDo.</p>

  <h2>Purchases</h2>
  <p>ToDo Pro is bought through Apple's In-App Purchase. Apple handles the payment and tells the
    app only whether a valid purchase exists. We never receive your name, your card, your address
    or your Apple Account, and there is no account on our side to attach any of it to. Apple's own
    privacy policy covers that transaction.</p>

  <h2>Children</h2>
  <p>ToDo collects no data from anyone, of any age.</p>

  <h2>Changes</h2>
  <p>If this policy ever changes, the date at the top changes with it. Any release that started
    collecting data would say so here first, and in the App Store privacy label.</p>

  <h2>Questions</h2>
  <p>Email <a href="mailto:nahidsaleem1@gmail.com">nahidsaleem1@gmail.com</a>.</p>
</div></section>'''


def main():
    render(out="todo/index.html",
           title="ToDo — a list that doesn't want your email address",
           description="A to-do app for iPhone with no account, no subscription and nothing "
                       "uploaded. Type a sentence and it becomes a task with the date and repeat "
                       "already set. The list is free forever; Pro is one payment of $29.99.",
           canonical="https://duneapps.com/todo/", og_type="product",
           body=BODY, style=PAGE_CSS + FAQ_CSS + """
  .btn.is-soon { opacity: .96; cursor: default; }
  .features .feat.card { padding: 26px 28px; }
""",
           og_image="og-todo.png", priority="0.9",
           head=faq_ld(FAQ) + '<script type="application/ld+json">' + json.dumps({
               "@context": "https://schema.org", "@type": "SoftwareApplication",
               "name": "ToDo: Productivity Planner",
               "applicationCategory": "ProductivityApplication",
               "operatingSystem": "iOS 17.0 or later",
               "description": "To-do list and daily planner for iPhone. No account, no "
                              "subscription, nothing uploaded. Quick add reads dates, times and "
                              "repeats out of plain English.",
               "offers": [{"@type": "Offer", "price": "0", "priceCurrency": "USD",
                           "description": "Free list, unlimited tasks, no account"},
                          {"@type": "Offer", "price": "29.99", "priceCurrency": "USD",
                           "description": "ToDo Pro, one payment, Family Sharing"}]}) + "</script>")
    print("page: todo/index.html")

    render(out="todo/privacy/index.html",
           title="ToDo privacy policy — nothing is collected",
           description="ToDo has no accounts, no analytics and no servers, and makes no network "
                       "connections. Your tasks stay on your iPhone.",
           canonical="https://duneapps.com/todo/privacy/",
           body=PRIVACY, style=PRIVACY_CSS, og_image="og-todo.png", priority="0.4")
    print("page: todo/privacy/index.html")


if __name__ == "__main__":
    main()
