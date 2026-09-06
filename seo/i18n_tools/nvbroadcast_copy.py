# -*- coding: utf-8 -*-
# Источники, проверенные 2026-09-06 на nvidia.com/en-us/geforce/broadcasting/broadcast-app/:
#   требования «NVIDIA GeForce RTX 2060, Quadro RTX 3000, TITAN RTX, or higher», Windows 10 64-bit,
#   драйвер R570+, 8 ГБ ОЗУ; карты GTX не поддерживаются;
#   эффекты микрофона: Noise Removal, Room Echo Removal, Studio Voice;
#   эффекты камеры: Virtual Background (removal/replacement/blur), Virtual Key Light, Eye Contact,
#   Video Noise Removal, Auto Frame; создаёт виртуальные камеру и микрофон; бесплатна;
#   САМА НЕ СТРИМИТ, не собирает сцены и не мультистримит — это слой улучшения поверх других программ.
# Наша сторона: ИИ-удаление фона работает без RTX — подтверждено владельцем 2026-09-06 (см. CLAUDE.md).
# 🔴 Честная граница: Eye Contact, Auto Frame, Studio Voice, Room Echo Removal и Virtual Key Light
# у нас отсутствуют. Это надо говорить прямо, а не обходить.
COPY = {
 "og": "og-nvidia-broadcast.png",
 "rival": "NVIDIA Broadcast",
 "title": "NVIDIA Broadcast Alternative — No RTX Needed | SplitCam",
 "description": ("NVIDIA Broadcast needs an RTX card and Windows. SplitCam removes your background "
                 "without one, runs on macOS too, and actually streams to 84+ platforms. Free."),
 "keywords": ("nvidia broadcast alternative, nvidia broadcast without rtx, nvidia broadcast for mac, "
              "free nvidia broadcast alternative, background removal without rtx, "
              "virtual background no green screen, nvidia broadcast gtx, streaming software no rtx"),
 "eyebrow": "NVIDIA Broadcast alternative",
 "h1_pre": "No RTX card? ",
 "h1_accent": "Your background can still go",
 "h1_post": ".",
 "sub": ("NVIDIA Broadcast is genuinely good, and it is free — but it asks for a GeForce RTX 2060 or "
         "better and Windows 10, and it does not stream anything itself. SplitCam removes your "
         "background with no card requirement and no green screen, runs on Windows and macOS, and "
         "goes live to 84+ platforms from the same window."),
 "badges": ["No RTX required", "Windows and macOS", "84+ platforms", "Free, no watermark"],
 "qa_h": "Short answer: these are two different tools",
 "qa": [
   "<strong>NVIDIA Broadcast is a filter layer.</strong> It improves one camera and one microphone, "
   "then offers them to other programs as virtual devices. It does not compose a scene, does not "
   "record and does not stream — NVIDIA says so plainly.",
   "<strong>SplitCam is the studio.</strong> Layers, scenes, a virtual camera, a virtual microphone, "
   "recording and multistreaming to 84+ destinations at once, from one window.",
   "<strong>The hardware line is the real fork.</strong> NVIDIA Broadcast requires a GeForce RTX 2060, "
   "Quadro RTX 3000 or TITAN RTX or higher. A GTX card will not do, and neither will a Mac. SplitCam "
   "asks for no particular card.",
   "<strong>You can run both.</strong> NVIDIA Broadcast publishes a camera device; SplitCam can take "
   "that device as a source. If you own the card, that combination is better than either alone.",
 ],
 "s1_h": "What NVIDIA Broadcast does better",
 "s1_p": ("Their filters are the product, and several have no counterpart here. If one of these is "
          "what you came for, install NVIDIA Broadcast — assuming your card qualifies."),
 "s1_cards": [
   ("Eye Contact",
    "Redirects your gaze so you appear to look into the lens while you read your notes. Nothing in "
    "SplitCam does this."),
   ("Auto Frame",
    "Tracks you and crops the picture so you stay centred as you move. SplitCam holds the framing "
    "you set."),
   ("Studio Voice and Room Echo Removal",
    "Reshapes a plain microphone toward a broadcast sound and strips reverb out of a bare room. "
    "SplitCam mixes and suppresses noise, but does neither of these."),
   ("Virtual Key Light and Video Noise Removal",
    "Relights your face to lift shadows and cleans up a grainy low-light picture. SplitCam has no "
    "relighting and no video denoiser."),
 ],
 "s2_h": "What SplitCam does that NVIDIA Broadcast does not",
 "s2_p": "Not better versions of the same thing — things the other tool does not attempt at all.",
 "s2_cards": [
   ("Background removal on any machine",
    "Real-time AI segmentation with no green screen, and no RTX requirement: it works on ordinary "
    "graphics, including integrated, and on Macs where an RTX card cannot exist."),
   ("Actually going live",
    "NVIDIA Broadcast hands its picture to another program and stops there. SplitCam streams to "
    "YouTube, Twitch, Facebook, Kick and 84+ destinations at once, direct to each platform."),
   ("Scenes made of many sources",
    "Cameras, a screen, a browser page, an IP camera, images, video and your phone, stacked as "
    "layers and switched live. NVIDIA Broadcast processes exactly one camera."),
   ("macOS",
    "NVIDIA Broadcast is a Windows application and needs an NVIDIA card. SplitCam runs natively on "
    "macOS 13 and later, including Apple Silicon."),
 ],
 "win_h": "The honest recommendation: use both if you can",
 "win_p": ("This is not a page trying to talk you out of a free NVIDIA tool. If you have a qualifying "
           "RTX card and you are on Windows, install NVIDIA Broadcast — Eye Contact and Studio Voice "
           "in particular have no equivalent here, and they are free. Then point SplitCam at the "
           "NVIDIA Broadcast camera as a source, and you get their per-frame polish inside a studio "
           "that can hold several sources and send the result to every platform at once. Where this "
           "page is genuinely the answer is the other case, and it is a large one: an integrated "
           "graphics chip, an older GeForce GTX, an AMD card, a work laptop, or a Mac. For any of "
           "those NVIDIA Broadcast will not install at all, and the choice is not between two tools "
           "but between having background removal and not having it."),
 "cmp_h": "SplitCam vs NVIDIA Broadcast",
 "cmp_p": ("NVIDIA figures are from nvidia.com, checked 6 September 2026. Requirements and the effect "
           "list change between versions — confirm on NVIDIA&#x27;s page before deciding."),
 "rows": [
   ("Price", "yes","Free, no watermark", "yes","Free"),
   ("Graphics card required", "yes","No particular card", "no","GeForce RTX 2060, Quadro RTX 3000 or TITAN RTX and up; GTX not supported"),
   ("Runs on macOS", "yes","Yes — macOS 13+", "no","Windows 10 64-bit only"),
   ("Background removal, no green screen", "yes","Yes", "yes","Yes — remove, replace or blur"),
   ("Eye contact correction", "no","No", "yes","Eye Contact"),
   ("Auto framing", "no","No", "yes","Auto Frame"),
   ("Face relighting", "no","No", "yes","Virtual Key Light"),
   ("Microphone noise suppression", "yes","Built into the mixer", "yes","Noise Removal"),
   ("Room echo removal", "no","No", "yes","Room Echo Removal"),
   ("Voice enhancement", "no","No", "yes","Studio Voice"),
   ("Virtual camera for other apps", "yes","60+ apps", "yes","Yes"),
   ("Scenes and layered sources", "yes","Unlimited layers, live switching", "no","One camera"),
   ("Streams to platforms", "yes","84+ at once, direct", "no","Does not stream"),
   ("Records", "yes","Yes", "no","No"),
 ],
 "faq": [
   ("Can I use NVIDIA Broadcast without an RTX card?",
    "No. NVIDIA lists a GeForce RTX 2060, Quadro RTX 3000 or TITAN RTX and above as the minimum, and "
    "GTX cards are not supported. If your card does not qualify, the app will not run — which is the "
    "situation this page is written for."),
   ("Is there an NVIDIA Broadcast for Mac?",
    "No. It is a Windows 10 64-bit application and it depends on an NVIDIA GPU, so a Mac cannot run "
    "it. SplitCam has a native macOS build, Apple Silicon included."),
   ("Does SplitCam remove the background without an RTX card?",
    "Yes. The AI segmentation does not require an RTX card — it works on ordinary graphics, including "
    "integrated chips, and on Macs. No green screen is needed either, though a physical chroma screen "
    "is still supported when you want the sharpest edge."),
   ("Can I use both at the same time?",
    "Yes, and it is a good setup if your card qualifies. NVIDIA Broadcast publishes a camera device; "
    "select that device as a source inside SplitCam, and its filters arrive in your scene before "
    "SplitCam composes and streams it."),
   ("Does NVIDIA Broadcast stream to Twitch or YouTube?",
    "No. NVIDIA describes it as working with your other apps — it improves the camera and microphone "
    "and hands them over. The streaming is done by whatever you point it at, which is where SplitCam "
    "or OBS comes in."),
   ("Does SplitCam have eye contact or auto framing?",
    "No to both. Eye Contact and Auto Frame are NVIDIA features with no equivalent here. If they are "
    "what you need and you have the card, run NVIDIA Broadcast — ideally feeding SplitCam."),
 ],
 "related": [
   ("https://splitcam.com/virtual-camera", "Virtual Camera",
    "How apps see the result", "The 60+ programs that accept SplitCam as a camera, and what they get."),
   ("https://splitcam.com/multistreaming", "Multistreaming",
    "84+ platforms at once", "How direct multistreaming works and what your upload needs to hold."),
   ("https://splitcam.com/alternatives", "Alternatives",
    "Compare the rest", "Where each streaming and webcam tool sits, including when it beats SplitCam."),
 ],
 "cta_h": "Background removal that does not check your graphics card.",
 "cta_p": "Free download for Windows and macOS. No RTX, no green screen, no subscription.",
}
