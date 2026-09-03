# -*- coding: utf-8 -*-
COPY = {
 "eyebrow": "Restream alternative",
 "title": "Free Restream Alternative — No Monthly Fee | SplitCam",
 "description": ("A free Restream alternative: SplitCam encodes on your own computer and sends each "
                 "stream straight to every platform. No cloud relay, no monthly plan."),
 "h1_pre": "A free ", "h1_accent": "Restream alternative",
 "h1_post": " that never leaves your computer.",
 "sub": ("Restream takes one stream from you, re-sends it from its servers, and bills you every month for "
         "the privilege. SplitCam encodes once on your machine and opens a connection to each platform "
         "itself — <strong>84+ destinations, nothing routed through anyone else, nothing to subscribe to</strong>."),
 "qa_h": "Quick answer — replacing Restream with SplitCam",
 "qa": [
   "Install SplitCam on the computer you already stream from. Windows 10/11 or macOS 13+.",
   "Add your destinations and paste each platform's stream key — 84+ are pre-configured.",
   "Set a bitrate per destination, or keep the defaults SplitCam picks for each platform.",
   "Run the built-in Upload Speed Test so you know your connection covers the total.",
   "Click Go Live. Every platform receives the stream directly from your machine.",
 ],
 "s1_h": "What the monthly fee actually buys",
 "s1_p": ("A cloud multistreaming service is a relay. You send it one stream, it holds a copy on its "
          "servers, and it forwards that copy to each platform you connected. The convenience is real, and "
          "so is the arrangement underneath: your broadcast passes through infrastructure you do not "
          "control, and the bill arrives whether you streamed four times that month or none."),
 "s1_cards": [
   ("Your stream makes a detour",
    "Every frame travels to the relay first and to your audience second. That is one more network hop and "
    "one more service that has to be up while you are live."),
   ("The bill is monthly, the streaming is not",
    "Published on our own site: Restream is $19/mo. A subscription charges for the calendar, not for the "
    "hours you actually broadcast."),
   ("Someone else decides the ceiling",
    "Quality, destination count and features are whatever tier you are on. Changing any of them is a "
    "pricing decision rather than a settings change."),
 ],
 "s2_h": "Your computer already does the encoding",
 "s2_p": ("The expensive part of streaming is encoding video, and your machine is already doing it. Once the "
          "frame is encoded, sending it to four platforms instead of one is just four network connections. "
          "SplitCam opens them itself — hardware encoding through NVENC, QuickSync or AMF on Windows and "
          "VideoToolbox on Mac, then a direct connection to each platform's ingest server."),
 "s2_cards": [
   ("Encode once, send many",
    "One encode feeds every destination, so adding a platform costs bandwidth rather than CPU."),
   ("Per-destination bitrate",
    "Want 6 Mbps to Twitch and 2.5 Mbps to Facebook? Set them separately instead of accepting one relay "
    "setting for everything."),
   ("Nothing between you and the platform",
    "If a platform is up and your connection is up, your stream is up. There is no third service that can "
    "have an outage on your behalf."),
   ("84+ platforms pre-configured",
    "Twitch, YouTube, Facebook, Kick, TikTok, X and the rest are already in the list with sensible defaults."),
 ],
 "win_h": "When Restream is the better pick",
 "win_p": ("This is the honest limit of sending directly, and it is worth knowing before you switch. "
           "A relay needs <strong>one</strong> upload from you. Sending directly needs the <strong>sum</strong> "
           "of every destination's bitrate leaving your house at once — four platforms at recommended "
           "settings is roughly 17 Mbps of upload. If your connection cannot hold that, a cloud relay is not "
           "a convenience, it is the thing that makes multistreaming possible at all. SplitCam ships an "
           "Upload Speed Test so you can check before you commit, and you can always run fewer destinations "
           "at lower bitrates — but if your upload is the constraint, Restream solves a problem SplitCam "
           "cannot. The same goes for streaming from a laptop on hotel or mobile internet, where the relay "
           "absorbs the instability instead of your audience seeing it."),
 "cmp_h": "SplitCam vs Restream — where each one sits",
 "cmp_p": "Honest table. The last two rows are the ones that should decide it for you.",
 "rows": [
   ("Price", "yes", "Free, no watermark", "no", "Free tier plus paid plans — check current pricing"),
   ("How the stream travels", "yes", "Direct from your machine to each platform", "meh", "Relayed from their cloud"),
   ("Destinations", "yes", "84+ pre-configured", "yes", "Multi-platform, plan-dependent"),
   ("Scene compositing on your machine", "yes", "Layers, sources, AI background, effects", "meh", "Studio is browser-based"),
   ("Virtual camera for Zoom / Teams / Meet", "yes", "Built in, 60+ apps", "no", "Not its purpose"),
   ("Works with no internet to a relay", "yes", "Local recording keeps working", "no", "The service is the product"),
   ("Upload bandwidth needed", "meh", "Sum of all destination bitrates", "yes", "One upload, fanned out for you"),
   ("Streaming from an unstable connection", "meh", "Your connection is the stream", "yes", "Relay absorbs the instability"),
 ],
 "faq": [
   ("Is SplitCam really a free Restream alternative?",
    "Yes, for the multistreaming part. SplitCam is free with no watermark and no subscription, and it "
    "multistreams to 84+ platforms. The difference is architectural, not a feature tier: SplitCam sends each "
    "stream from your computer instead of relaying it from a cloud service."),
   ("Do I need more upload bandwidth than with Restream?",
    "Yes, and this is the main thing to check. A relay takes one upload from you; sending directly needs the "
    "sum of all destination bitrates leaving at once — about 17 Mbps for four platforms at recommended "
    "settings. SplitCam has a built-in Upload Speed Test, so you can find out in a minute rather than "
    "discover it mid-stream."),
   ("Can I keep using my existing stream keys?",
    "Yes. Each destination takes the same stream key the platform gives you. Nothing about your channels or "
    "their settings changes — only where the connection originates."),
   ("What happens to my scenes and overlays?",
    "You build them in SplitCam itself: layered sources on one canvas, AI background removal, effects, "
    "browser sources for overlays. If you are coming from OBS as well, SplitCam imports OBS scene "
    "collections in one click."),
   ("Does it record while streaming?",
    "Yes, locally on your own machine, and that keeps working regardless of what any online service is "
    "doing at the time."),
   ("Is there a catch with the free version?",
    "No account to create, no time limit and no watermark. SplitCam has been free since 2003 and the "
    "current version is v10.9.2."),
 ],
 "cta_h": "Multistream without the monthly bill",
 "cta_p": ("Free download, Windows 10/11 and macOS 13+. Check your upload with the built-in speed test, paste "
           "your keys, and the relay stops being part of your setup."),
}
