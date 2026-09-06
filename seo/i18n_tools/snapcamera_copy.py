# -*- coding: utf-8 -*-
# Snap Camera закрыт 25 января 2023: Snap выключил серверы авторизации, из-за чего приложение
# перестало работать даже у тех, кто уже установил его. Источники: TechCrunch 05.01.2023,
# Adweek. Спрос осиротел — вендора, который защищал бы выдачу, больше нет.
# 🔴 Честная граница: у SplitCam НЕТ экосистемы линз (Lens Studio, каталог AR-линз сообщества).
# Есть бьюти-ретушь, цветовые фильтры, маски и оверлеи, ИИ-фон — и виртуальная камера, которой
# всё это доставляется в 60+ приложений. Обходной путь для тех, кому нужны именно линзы Snapchat:
# Snapchat for Web работает в браузере, а браузерное окно SplitCam умеет брать источником сцены.
COPY = {
 "og": "og-snap-camera.png",
 "rival": "Snap Camera",
 "title": "Snap Camera Alternative — Free Filters | SplitCam",
 "description": ("Snap Camera shut down in January 2023. SplitCam is a free alternative: beauty, "
                 "filters, masks and AI backgrounds, sent to Zoom, Teams and Meet as a webcam."),
 "keywords": ("snap camera alternative, free snap camera alternative, snap camera replacement, "
              "snap camera shut down, webcam filters, video call filters, beauty filter webcam, "
              "virtual camera with filters, snap camera for zoom"),
 "eyebrow": "Snap Camera alternative",
 "h1_pre": "Snap Camera is gone. ",
 "h1_accent": "Your filters do not have to be",
 "h1_post": ".",
 "sub": ("Snap shut the app down on 25 January 2023 and switched off the servers that loaded its "
         "lenses, so it stopped working even for people who already had it installed. SplitCam does "
         "the part that mattered in a video call — a polished face and a clean background, handed to "
         "Zoom, Teams, Meet or Discord as an ordinary webcam. Free, on Windows and macOS, still updated."),
 "badges": ["Free, no watermark", "Windows and macOS", "Works as a webcam in 60+ apps", "Still maintained"],
 "qa_h": "Short answer: what carries over and what does not",
 "qa": [
   "<strong>Reinstalling Snap Camera will not work.</strong> Snap turned off the authentication "
   "servers the app used to load lenses. An old installer still launches, and then has nothing to load.",
   "<strong>What carries over</strong> is the mechanism: a virtual camera that video apps see as a "
   "normal webcam. SplitCam registers the same way, so Zoom, Teams, Meet, Discord and OBS pick it "
   "up from the ordinary camera dropdown.",
   "<strong>What carries over in looks</strong> is beauty and skin smoothing, colour filters, masks "
   "and overlays, plus background removal with no green screen. Applied live, on the GPU.",
   "<strong>What does not carry over</strong> is Snap&#x27;s lens catalogue. SplitCam is not a lens "
   "platform: there is no Lens Studio, no community lens library, and none of the specific viral "
   "lenses. If a particular Snapchat lens is the reason you are here, read the section below on "
   "Snapchat for Web.",
 ],
 "s1_h": "What you genuinely lose",
 "s1_p": ("Snap Camera was a window into an AR platform, not just a filter box. That platform is not "
          "something SplitCam has, and pretending otherwise would waste your afternoon."),
 "s1_cards": [
   ("The lens catalogue",
    "Snap Camera pulled from a library of community-built lenses — the potato, the cat, thousands of "
    "others. SplitCam ships a fixed set of effects, masks and overlays. There is no catalogue to browse "
    "and no creator marketplace behind it."),
   ("Lens Studio and custom AR",
    "Snap had an authoring tool: build a lens, publish it, use it in the desktop app. SplitCam has no "
    "equivalent. You cannot author a face-tracked AR object and load it in."),
   ("Deep face-tracked AR",
    "Snap&#x27;s lenses tracked facial geometry closely enough to place 3D objects, warp features and "
    "react to expressions. SplitCam&#x27;s masks and overlays are simpler than that."),
   ("The Snapchat account tie-in",
    "Lenses you had saved in Snapchat followed you into Snap Camera. Nothing in SplitCam connects to "
    "a Snapchat account."),
 ],
 "s2_h": "What replaces it, free",
 "s2_p": "The parts of Snap Camera that people actually used in meetings and streams, on a tool that is still maintained.",
 "s2_cards": [
   ("A webcam any app accepts",
    "The same trick Snap Camera used: SplitCam appears in the camera list of Zoom, Microsoft Teams, "
    "Google Meet, Discord, OBS and 60+ other apps. Nothing to integrate — pick it from the dropdown."),
   ("Beauty, filters and masks, live",
    "Skin smoothing and beauty retouch, colour filters, masks and overlays, applied on the GPU while "
    "you talk, and sent straight to the call and to your stream."),
   ("Backgrounds without a green screen",
    "Real-time AI segmentation cuts you out of the room: swap in an image or video, blur the room, or "
    "key a physical chroma screen when you want the sharpest edge. Snap Camera had no equivalent depth here."),
   ("More than a face",
    "Screens, browser pages, a second camera and your phone can share the frame as layers, and you can "
    "switch scenes live. Snap Camera did one camera and one lens."),
 ],
 "win_h": "If you specifically want a Snapchat lens",
 "win_p": ("Be honest with yourself about what you are after. If the whole point is one particular lens — "
           "the one your team laughs at every standup — no desktop app brings it back, because the "
           "desktop product is gone and its servers with it. What still exists is Snapchat itself: the "
           "web version runs lenses in a browser. That gives you a practical route rather than a "
           "replacement: open Snapchat for Web, then add that browser window to a SplitCam scene as a "
           "source and send the scene onward as your webcam. It is more setup than Snap Camera was, the "
           "lens set is not identical, and it depends on Snap keeping the web app running. For everything "
           "that is not a specific lens — looking good on camera, hiding the room behind you — SplitCam "
           "is the shorter path, and it does not depend on anyone&#x27;s servers staying up."),
 "cmp_h": "SplitCam vs Snap Camera",
 "cmp_p": ("Snap Camera is discontinued, so its column describes the app as it was until 25 January 2023. "
           "Shutdown reported by TechCrunch on 5 January 2023 and by Adweek."),
 "rows": [
   ("Still works today", "yes","Yes, actively updated", "no","No — discontinued 25 January 2023"),
   ("Price", "yes","Free, no watermark", "meh","Was free, while it lasted"),
   ("Windows and macOS", "yes","Both", "meh","Both, until shutdown"),
   ("Virtual camera for video apps", "yes","60+ apps, from the camera dropdown", "yes","That was its whole purpose"),
   ("Community lens catalogue", "no","No lens library", "yes","Thousands of lenses from creators"),
   ("Custom AR authoring", "no","No", "yes","Lens Studio"),
   ("Beauty and skin smoothing", "yes","Built in", "meh","Through certain lenses"),
   ("Colour filters, masks, overlays", "yes","Built in", "yes","Through lenses"),
   ("AI background removal", "yes","Real time, no green screen", "meh","Some lenses only"),
   ("Multiple sources in one frame", "yes","Cameras, screens, browser, phone", "no","One camera"),
   ("Streams to platforms directly", "yes","84+ destinations at once", "no","Not a streaming tool"),
   ("Depends on a vendor&#x27;s servers", "yes","No — runs locally", "no","Yes, and that is what ended it"),
 ],
 "faq": [
   ("Why did Snap Camera stop working?",
    "Snap discontinued it on 25 January 2023 and switched off the authentication servers it used to "
    "load lenses. Because that check happened at startup, the app stopped working even on machines "
    "where it was already installed."),
   ("Can I still download Snap Camera?",
    "Old installers circulate, but they do not restore the product: the servers the app talked to are "
    "gone, so it has no lenses to fetch. Treat any site offering it today with suspicion."),
   ("What is the closest free Snap Camera alternative?",
    "For the everyday use — looking good on a call and hiding your room — SplitCam covers it: beauty "
    "and skin smoothing, colour filters, masks and overlays, and AI background removal, delivered to "
    "Zoom, Teams, Meet and Discord as a normal webcam. For the AR lens catalogue specifically, nothing "
    "free replaces it one for one."),
   ("Does SplitCam have Snapchat lenses?",
    "No. SplitCam is not a lens platform and has no connection to Snapchat. It has its own effects, "
    "masks and overlays. If you need actual Snapchat lenses, Snapchat for Web runs in a browser, and "
    "you can add that browser window to a SplitCam scene as a source."),
   ("Will it work in Zoom, Teams and Google Meet?",
    "Yes. SplitCam registers as a camera device, so those apps list it alongside your real webcam. "
    "Pick SplitCam in the video settings and whatever you have composed becomes your picture."),
   ("Is it really free?",
    "Yes — no watermark, no time limit and no subscription. That includes the effects, the background "
    "removal and the virtual camera."),
 ],
 "related": [
   ("https://splitcam.com/virtual-camera", "Virtual Camera",
    "How apps see the result", "The 60+ programs that accept SplitCam as a camera, and what they get."),
   ("https://splitcam.com/alternatives/manycam", "ManyCam alternative",
    "The webcam-tool comparison", "Effects, a virtual camera and the price gap, side by side."),
   ("https://splitcam.com/alternatives", "Alternatives",
    "Compare the rest", "Where each streaming and webcam tool sits, including when it beats SplitCam."),
 ],
 "cta_h": "Put your face back on camera.",
 "cta_p": "Free download for Windows and macOS. No account, no lens store, no shutdown notice.",
}
