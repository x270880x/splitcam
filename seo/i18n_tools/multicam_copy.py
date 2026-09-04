# -*- coding: utf-8 -*-
# Опора: /features/ («Stack and arrange layers, then switch scenes live», «Unlimited layered
# sources per scene»), changelog («three or more IP-Cams work correctly when added to one scene»;
# переходы Fade, Stinger, Luma Wipe, Slide, Swipe; Phone Camera 10.7.20; Stream Deck 10.8.25),
# /for/educators/ (Phone Camera и захват окна на macOS 13+; Windows-only: Whiteboard, Application
# Audio, Replay, Color), владелец (хоткеи на macOS; QR-связывание через сервер, видео — нет).
# ЗАПРЕЩЕНО: любое число камер, «unlimited scenes», 64, PTZ, ISO, Preview/Program, multiview,
# NDI out, автопереключение, гости по ссылке.
COPY = {
 "og": "og-multi-camera.png",
 "rival": "macOS",
 "cols": ["Source", "Windows", "macOS"],
 "crumb3": "Multi-camera streaming", "crumb3_short": "Multi-camera",
 "faq_h": "Multi-camera streaming — questions",
 "title": "Free Multi-Camera Live Streaming Software | SplitCam",
 "description": ("Free multi-camera live streaming software for Windows and Mac: switch cameras live or show two at once. Webcams, IP cameras, NDI and your phone in one scene."),
 "keywords": ("multi camera live streaming software, multi camera live streaming software free, "
              "free multi camera live streaming software, multicam streaming software, multi camera software, "
              "live stream multiple cameras, two cameras one stream"),
 "eyebrow": "Multi-camera streaming",
 "h1_pre": "Free multi-camera live streaming software — ",
 "h1_accent": "switch between cameras, or show them at once",
 "h1_post": ".",
 "sub": ("«Multi-camera» means two different things, and people search for both with the same words. "
         "One is switching: one camera in the frame, and you choose which. The other is composing: two "
         "cameras in the frame together. SplitCam does both with the same two ideas — layers inside a "
         "scene, and scenes you switch between live — on Windows and macOS, for free."),
 "badges": ["Free, no watermark", "Webcam, IP, NDI, phone", "Windows and macOS", "Hotkeys and Stream Deck"],
 "qa_h": "Set up in four steps",
 "qa": [
   "<strong>Add your cameras as layers.</strong> USB webcams, IP cameras over RTSP, an NDI source, or your "
   "phone through the Phone Camera source. Each one becomes a layer you can place and resize.",
   "<strong>Build one scene per shot.</strong> A wide shot, a close-up, a slide with a small camera in the "
   "corner. A scene is just an arrangement of layers; make as many as your show needs.",
   "<strong>Switch scenes live.</strong> Click the scene, press its hotkey, or press a button on a Stream "
   "Deck or on the SplitCam Remote app on your phone. Pick a transition: cut, fade, slide, wipe or a stinger.",
   "<strong>Send the result anywhere.</strong> To 84+ platforms at once, to a recording, or into Zoom, Teams "
   "and Meet through the virtual camera — they see whichever scene is live.",
 ],
 "s1_h": "Switching: one camera in the frame, you pick which",
 "s1_p": ("This is the director&#x27;s job — wide, close, wide again. In SplitCam it is one scene per shot "
          "and a switch between them."),
 "s1_cards": [
   ("A scene is a shot",
    "Put the wide camera in one scene and the close-up camera in another. Switching shots is switching "
    "scenes, and the audience sees a clean cut rather than a layer being dragged around."),
   ("Transitions between them",
    "Cut, fade, slide, swipe, luma wipe, or a stinger — your own animated wipe. The transition is a "
    "property of the switch, so the same scene can be entered differently from different places."),
   ("Switch without the mouse",
    "Put each scene on a hotkey, on Windows or macOS. If you own a Stream Deck, SplitCam supports it on "
    "Windows since build 10.8.25. The free SplitCam Remote app on an iPhone does the same from across the room."),
   ("Multiple IP cameras in one show",
    "Three or more IP cameras in a single scene is a documented, tested configuration. Each is a layer; "
    "each can be in as many scenes as you like."),
 ],
 "s2_h": "Composing: two cameras in the frame at once",
 "s2_p": ("Picture-in-picture, side by side, a camera over a screen share. No switching at all — this is "
          "layers stacked inside one scene."),
 "s2_cards": [
   ("Stack, place, resize",
    "Every source is a layer with a position and a size. Drop the second camera into a corner of the "
    "first, or split the frame down the middle. What you see on the canvas is what goes out."),
   ("Camera over anything",
    "The second layer does not have to be a camera. A slide, a browser page, a full-screen game or a "
    "window capture underneath, your face on top — the same mechanism."),
   ("Your phone as the second angle",
    "Add a Phone Camera source, scan the QR code, and the phone joins with video and audio through its "
    "browser — nothing to install on it. Prop it on a small tripod for the overhead or the wide."),
   ("Both at once in a video call",
    "Select SplitCam as the camera in Zoom, Teams or Meet and the call receives the composed scene: two "
    "cameras, or a camera and a slide, as one picture."),
 ],
 "win_h": "What SplitCam does not do for multi-camera work",
 "win_p": ("Be clear about the ceiling before you build a show on it. There is no Preview/Program — you "
           "switch straight to a scene, you do not cue it first — and no multiview wall of source previews. "
           "Recording captures the composed scene as one file, not each camera separately for the edit. "
           "Nothing pans, tilts or zooms a camera for you. NDI comes in but does not go out. There is no "
           "automatic switching to whoever is speaking, and no browser link for a remote guest. If your "
           "production needs any of that, it needs a broadcast switcher — vMix on Windows, or a hardware "
           "ATEM — and this page is not going to talk you out of it. If it needs cameras in scenes and "
           "scenes switched cleanly, that is exactly what is here."),
 "cmp_h": "Which sources join, on which system",
 "cmp_p": ("The core — scenes, layers, switching, the virtual camera, recording and multistreaming — runs "
           "on both Windows 10/11 and macOS 13+. A few sources are documented on Windows only."),
 "rows": [
   ("USB webcams", "yes","Yes", "yes","Yes"),
   ("IP cameras over RTSP", "yes","Yes", "yes","Yes"),
   ("NDI (as an input)", "yes","Yes", "yes","Yes"),
   ("Phone Camera (browser, QR)", "yes","Yes", "yes","Yes"),
   ("Screen and window capture", "yes","Yes", "yes","Yes"),
   ("Browser page, images, video files", "yes","Yes", "yes","Yes"),
   ("Scene hotkeys", "yes","Yes", "yes","Yes"),
   ("Stream Deck", "yes","Yes, since 10.8.25", "meh","Not documented on macOS"),
   ("Whiteboard, Application Audio, Replay, Color source", "yes","Yes", "no","Windows only"),
 ],
 "faq": [
   ("Is this really free multi-camera live streaming software?",
    "Yes. Scenes, layers, switching with transitions, the virtual camera, recording and multistreaming to "
    "84+ platforms are all in the free download, with no watermark and no paid tier above it."),
   ("How many cameras can I use?",
    "SplitCam does not publish a fixed limit, and we will not invent one here. Three or more IP cameras in "
    "one scene is a documented configuration; in practice the ceiling is your computer&#x27;s CPU, GPU and "
    "USB bandwidth, not a number in the software."),
   ("What is the difference between switching and showing two cameras at once?",
    "Switching is one camera in the frame at a time — separate scenes, and you cut between them. Showing "
    "two at once is layers inside one scene — picture-in-picture or side by side. SplitCam does both; "
    "which one you want decides whether you build several scenes or one."),
   ("Can I switch cameras without touching the keyboard?",
    "Yes. Each scene can have a hotkey on Windows and macOS; a Stream Deck is supported on Windows; and "
    "the free SplitCam Remote app switches scenes from an iPhone."),
   ("Does it record each camera separately?",
    "No. Recording captures the composed scene as one file. If you need every camera as its own file for "
    "editing, that is ISO recording, and it needs a broadcast switcher such as vMix."),
   ("Does the phone camera need an app?",
    "No. Add a Phone Camera source, scan the QR code with the phone, and it joins through its browser with "
    "video and audio. The pairing goes through SplitCam&#x27;s servers to introduce the two devices; the "
    "video then flows between your phone and your computer."),
   ("Does multi-camera work on a Mac?",
    "Yes — scenes, layers, switching, hotkeys, the Phone Camera source, recording and the virtual camera run "
    "on macOS 13 and later. The Whiteboard, Application Audio, Replay and Color sources are documented on "
    "Windows only."),
 ],
 "related": [
   ("https://splitcam.com/phone-as-webcam", "Phone Camera",
    "Your phone as a camera", "How the QR pairing works and when a dedicated webcam app is the better choice."),
   ("https://splitcam.com/alternatives/vmix", "vMix alternative",
    "When you need the broadcast suite", "Preview/Program, ISO, PTZ — what vMix has and this does not."),
   ("https://splitcam.com/multistreaming", "Multistreaming",
    "Send the show everywhere", "84+ platforms at once and what your upload needs to hold."),
 ],
 "cta_h": "Two cameras, one free program.",
 "cta_p": "Download for Windows and macOS. Build a scene per shot and switch.",
}
