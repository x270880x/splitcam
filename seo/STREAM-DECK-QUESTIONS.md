# Stream Deck × SplitCam — что подтверждено и что спросить у разработчика (2026-09-05)

## Подтверждено (с источниками)
- Официальный плагин «SplitCam» в Elgato Marketplace, автор @splitcam, бесплатный, Windows 10+,
  требует Stream Deck 6.9+. Версии: 1.0 (22.10.2024), 1.1 (02.01.2025, список сцен из SplitCam),
  1.2 (10.07.2026, фикс переключения сцен).
  https://marketplace.elgato.com/product/splitcam-5231d1ca-5a53-417b-b6b7-48a690fe3915
- Действия: Start/Stop Stream · Switch Scene · Start/Stop Recording · Pause Scene · Mute · Snapshot;
  таймер сессии на кнопке; кнопки отражают статус; работает в Multi Action.
- Changelog Windows v10.8.25 (18.01.2025): «Added Stream Deck support» — единственное упоминание на сайте.
- В splitcam.exe 10.9.2: классы streamdeck::CStreamDeckFileMapping, ui::CStreamDeckListener —
  связь через shared memory + event, не WebSocket. В инсталляторе плагина нет — он ставится из Marketplace.
- Ролик: «How to Set Up SplitCam with Elgato Stream Deck – Complete Guide», канал @SplitCamSoftware,
  28.11.2024, 222 просмотра. https://www.youtube.com/watch?v=WCfaMpOlFDY

## Вопросы
1. Плагин 1.0 вышел 22.10.2024, а «Added Stream Deck support» в changelog — 10.8.25 от 18.01.2025.
   Какая версия SplitCam реально первая с поддержкой? (На странице написано «10.8.25 or newer» — консервативно.)
2. Точные названия действий в панели Stream Deck и их число — шесть из описания или больше?
3. Нужно ли что-то включать в SplitCam (галочка/настройка), или связь работает всегда при запуске?
4. macOS: планируется ли плагин? Сейчас — Windows only, на Mac только SplitCam Remote.
5. Полный список хоткеев SplitCam (Windows) — для запасного пути через стандартное действие «Hotkey».
6. Ролик 2024 года актуален для плагина 1.2? В описании ролика — «layers, effects, transitions», которых в плагине нет.
7. Почему плагин нигде не упомянут на сайте и в UI — забыли или намеренно? Сейчас упомянут на
   /alternatives/stream-deck/ и /multi-camera/; стоит добавить на /products/ и /features/.
8. Кто сопровождает плагин и есть ли репозиторий — для поддержки пользователей.
