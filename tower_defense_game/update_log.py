QOL_CENTURY_DETAILS = """
Added a FULL HUD detail preset in Settings.
Added a CLEAN HUD detail preset in Settings.
FULL preset restores path direction arrows.
FULL preset restores enemy health bars.
FULL preset restores difficulty threat marks.
FULL preset restores selected tower range display.
FULL preset restores tower target links.
FULL preset restores floating combat text.
FULL preset restores the match statistics panel.
CLEAN preset hides path direction arrows.
CLEAN preset hides enemy health bars.
CLEAN preset hides difficulty threat marks.
CLEAN preset hides selected tower ranges.
CLEAN preset hides tower target links.
CLEAN preset hides floating combat labels.
CLEAN preset hides the match statistics panel.
Added H as an in-match match-stats toggle.
Added J as an in-match target-link toggle.
Added K as an in-match enemy-health-bar toggle.
Added O as an in-match floating-text toggle.
Added Y as an in-match path-arrow toggle.
Added T as an in-match threat-mark toggle.
Added on-screen confirmation when match stats are toggled.
Added on-screen confirmation when target links are toggled.
Added on-screen confirmation when health bars are toggled.
Added on-screen confirmation when floating text is toggled.
Added on-screen confirmation when path arrows are toggled.
Added on-screen confirmation when threat marks are toggled.
Added Escape to clear the current selection.
Added C to clear the current selection.
Added 0 to clear the current selection.
Added a selection-cleared confirmation notice.
Added Tab to cycle through build choices.
Tab cycling includes the Arrow tower.
Tab cycling includes the Cannon tower.
Tab cycling includes the Frost tower.
Tab cycling includes the Sniper tower.
Tab cycling includes the Laser tower.
Tab cycling includes the Mortar tower.
Tab cycling includes the Venom tower.
Tab cycling includes the Storm tower.
Tab cycling includes the selected special tower.
Added Enter as a start-wave shortcut.
Space can now pause during an active wave.
Space can now resume during an active wave.
Added a pause confirmation notice.
Added a resume confirmation notice.
Added a wave-start confirmation notice.
Added comma to decrease playback speed.
Added period to increase playback speed.
Speed stepping now supports a 3x upper setting.
Speed changes now produce a confirmation notice.
Auto-pause changes now produce a confirmation notice.
Added a clickable special-tower toolbar button.
Special toolbar button shows the selected special color.
The special toolbar button marks itself unavailable after use.
Added toolbar hover details for Arrow.
Added toolbar hover details for Cannon.
Added toolbar hover details for Frost.
Added toolbar hover details for Sniper.
Added toolbar hover details for Laser.
Added toolbar hover details for Mortar.
Added toolbar hover details for Venom.
Added toolbar hover details for Storm.
Added toolbar hover details for the special tower.
Toolbar hover details show difficulty-adjusted hit damage.
Toolbar hover details show range.
Toolbar hover details show purchase cost.
Toolbar hover details show affordability status.
Toolbar hover details show slow capability.
Toolbar hover details show splash capability.
Toolbar hover details show poison capability.
Unaffordable Arrow buttons are visibly dimmed.
Unaffordable Cannon buttons are visibly dimmed.
Unaffordable Frost buttons are visibly dimmed.
Unaffordable Sniper buttons are visibly dimmed.
Unaffordable Laser buttons are visibly dimmed.
Unaffordable Mortar buttons are visibly dimmed.
Unaffordable Venom buttons are visibly dimmed.
Unaffordable Storm buttons are visibly dimmed.
Added a square highlight around a selected tower.
Selected tower panels now display current hit damage.
Selected tower panels now display current range.
Selected tower panels now display current cooldown.
Added a clickable Power upgrade button to the tower panel.
Added a clickable Speed + Range upgrade button.
Added a clickable Sell button to the tower panel.
Click upgrades update spent-money statistics.
Click upgrades update total-upgrades statistics.
Sold towers preserve their damage in match totals.
Added total match kill tracking.
Tracked total damage across active and sold towers.
Added total earned-money tracking.
Added total spent-money tracking.
Added total built-tower tracking.
Added total upgraded-tower tracking.
Added total leaked-enemy tracking.
Added a compact match-statistics overlay.
Added warning halos for enemies close to the exit.
Added start and goal path endpoint markers for route clarity.
""".strip().splitlines()

VISUAL_FINISH_DETAILS = """
Added a darker drop shadow beneath reusable menu buttons.
Added a fine upper highlight edge to reusable menu buttons.
Added a gold side marker to selected menu buttons.
Added depth shadows beneath in-game purchase buttons.
Added colored lower rails to affordable tower buttons.
Added subdued lower rails to unavailable tower buttons.
Framed selected purchase buttons with a bright edge.
Added a gold trim bar to the home-screen action panel.
Added a gold trim bar to the home-screen update panel.
Added a PLAY label to organize the home-screen actions.
Aligned the visual treatment of the home menu and update log.
Added a bright top accent line to standard menu backgrounds.
Added an inset border to standard menu backgrounds.
Improved visual framing on the Settings screen.
Improved visual framing on the Controls screen.
Improved visual framing on the difficulty screen.
Improved visual framing on dictionary screens.
Improved visual framing on detail inspection screens.
Improved visual framing on the special tower selection screen.
Added separator lines between home-screen update entries.
Added gold entry markers beside visible update entries.
Preserved five-entry update pages inside the refined frame.
Kept update navigation seated within the panel footer.
Added shadow depth to special tower choice rows.
Added role-colored rails to special tower choice rows.
Added an accent bar to the special tower showcase stage.
Added shadow depth to character dictionary entries.
Added bright glints to dictionary color swatches.
Added role-colored rails to dictionary entries.
Added a bright stage trim line to character previews.
Added a lit center to the character preview pedestal.
Added start-point markers to mini-map previews.
Added exit-point markers to mini-map previews.
Added extra grass sprout detail variation to battlefields.
Added a subtle frame around the active battlefield.
Added a lighter center trace along detailed roads.
Strengthened the visible road entrance marker.
Filled the entrance marker for better contrast.
Added an entrance-direction arrow glyph.
Strengthened the visible road exit marker.
Filled the exit marker for better contrast.
Added a square goal glyph at the road exit.
Preserved moving road glints above the new road detail.
Preserved directional arrows above the clarified path.
Added framed health-bar backgrounds for enemies.
Added fine borders around enemy health bars.
Added a highlight streak to remaining enemy health.
Kept critical-health bars strongly red.
Kept mid-health bars visibly yellow.
Kept healthy bars visibly green.
Added a flashing warning chevron to near-exit enemies.
Retained the near-exit warning ring beneath the chevron.
Added visible poison bubbles to poisoned enemies.
Added visible frost marks to slowed enemies.
Preserved enemy ground shadows below status effects.
Preserved animated enemy movement while status effects render.
Added a brighter inner streak to laser fire.
Added impact rings to detailed projectile hits.
Added a trailing shadow to airborne shell shots.
Added diagonal crystal detail to frost shots.
Added liquid highlights to venom droplets.
Added fletching detail to arrow shots.
Preserved lightning forks for storm attacks.
Preserved shell arcs for cannon and mortar attacks.
Added dark backing panels behind floating combat labels.
Kept particle cores visible inside expanding hit rings.
Added an inner placement circle to build previews.
Preserved valid placement outlines with improved focus.
Preserved invalid placement crosses over the new focus ring.
Preserved tower range previews around proposed builds.
Added colored platform rings beneath standard towers.
Added colored platform rings beneath special towers.
Added an outline around tower ground shadows.
Added a gem light on each tower plinth.
Added a bright model glint to placed towers.
Added trim to the Arrow tower hood.
Added highlighted wheel hubs to the Cannon tower.
Added an icy focus ring to the Frost tower.
Added a glowing lens point to the Sniper tower.
Added an energy ring to the Laser tower core.
Added a reinforced brace to the Mortar tower.
Added a glowing vessel ring to the Venom tower.
Added a charged halo to the Storm tower.
Preserved upgrade orbit marks above the refined tower bases.
Preserved special tower aura rings above the refined bases.
Added visual separators between top HUD resource groups.
Added a bright moving cap to wave progress.
Added a framed match-state badge for ready, paused, and speed.
Added a backing strip beneath the active build summary.
Added a colored accent line to match-stat panels.
Added colored accent ticks to on-screen notices.
Added a color rail to the selected-tower panel.
Added a tower-color identifier dot to that panel.
Added four-step power upgrade pips to selected towers.
Added four-step utility upgrade pips to selected towers.
Distinguished filled upgrade pips from remaining slots.
Added compass markers around selected tower ranges.
Added a colored header rail to toolbar hover details.
Added a full outline around the game-over dialog.
Unified panels, selections, feedback, and models.
""".strip().splitlines()


UPDATE_LOG = [
    {
        "version": "1.6.0",
        "title": "3D Maps Collection",
        "notes": [
            "All ten maps now have playable 3D editions.",
            "A new 3D tab houses raised-terrain battlefields.",
        ],
        "details": [
            "Added a dedicated 3D map collection beside Classic and Polished.",
            "Created a playable 3D edition for each of the ten layouts.",
            "Preserved original paths, economies, lives, and placement rules.",
            "Kept reliable top-down targeting and build coordinates.",
            "Built elevated roads with highlighted tops and visible side depth.",
            "Added raised battlefield framing and elevated island build pads.",
            "Carried the detailed animated environments into the 3D editions.",
            "Added 3D selection and dictionary tabs.",
            "Added raised-terrain miniature previews for every 3D map.",
            "Extended keyboard map 10 selection across every collection.",
        ],
    },
    {
        "version": "1.5.9",
        "title": "Polished Maps: Crystal Cavern",
        "notes": [
            "Polished Crystal Cavern completes the remastered collection.",
            "Glowing formations and underground pools animate the cave.",
        ],
        "details": [
            "Added Polished Crystal Cavern as the tenth polished battlefield.",
            "Preserved Crystal Cavern's path, treasure bonus, lives, and rewards.",
            "Replaced square tiles with layered subterranean stone chambers.",
            "Added luminous mineral clusters with gently pulsing highlights.",
            "Built reflective turquoise cave pools and drifting light motes.",
            "Added stalactites, a luminous cave fall, and splashing glow.",
            "Added mine rails, an abandoned cart, and glowing mushrooms.",
            "Changed the road into a glowing crystal-edged cavern route.",
            "Added a dedicated polished dictionary preview.",
        ],
    },
    {
        "version": "1.5.8",
        "title": "Polished Maps: Retro Grid",
        "notes": [
            "Polished Retro Grid becomes a living synthwave cityscape.",
            "Neon route lighting moves beneath a sunset skyline.",
        ],
        "details": [
            "Added Polished Retro Grid as its own playable remaster.",
            "Preserved Retro Grid's original route, income, and wave bonus.",
            "Built a dark synthwave horizon with skyline silhouettes.",
            "Added a striped neon sun, star lights, and moving scan glow.",
            "Added a perspective neon floor and animated tower windows.",
            "Added a glowing billboard and flying light-trail traffic.",
            "Added old-TV scanlines, rolling static bands, and signal glitches.",
            "Changed the path into a bright neon-lit continuous route.",
            "Added a dedicated polished dictionary preview.",
        ],
    },
    {
        "version": "1.5.7",
        "title": "Polished Maps: Miami Beach",
        "notes": [
            "Polished Miami Beach opens along a bright neon shoreline.",
            "Surf, palms, umbrellas, and skyline details animate the coast.",
        ],
        "details": [
            "Added Polished Miami Beach as a separate beach remaster.",
            "Preserved Miami Beach's route and high-money economy.",
            "Built moving turquoise surf along a continuous sandy shore.",
            "Added resort palms, beach umbrellas, and illuminated towers.",
            "Changed the route into a bright coastal promenade.",
            "Added a dedicated polished dictionary preview.",
        ],
    },
    {
        "version": "1.5.6",
        "title": "Polished Maps: Warzone",
        "notes": [
            "Polished Warzone becomes a scarred trench battlefield.",
            "Cratered mud, wire, bunker lines, and smoke fill the field.",
        ],
        "details": [
            "Added Polished Warzone while preserving its extra-life rules.",
            "Retained the original route, money, and wave economy.",
            "Painted continuous muddy terrain with shell craters.",
            "Added bunker sandbags, barbed wire, and lifting smoke columns.",
            "Added destroyed armor, duckboards, lamps, and shell flashes.",
            "Changed the road into a worn trenchland supply route.",
            "Added a dedicated polished dictionary preview.",
        ],
    },
    {
        "version": "1.5.5",
        "title": "Polished Maps: Race Track Loop",
        "notes": [
            "Polished Race Track Loop becomes a floodlit circuit.",
            "Grandstands, pit lane, flags, and turf surround the course.",
        ],
        "details": [
            "Added Polished Race Track Loop as a circuit remaster.",
            "Preserved its looping route, reward bonus, and gameplay rules.",
            "Built continuous infield turf, grandstand seating, and pit garages.",
            "Added floodlights and animated checkered race details.",
            "Added a timing tower, tire walls, podium, and pace light.",
            "Changed the enemy route into a clean asphalt circuit.",
            "Added a dedicated polished dictionary preview.",
        ],
    },
    {
        "version": "1.5.4",
        "title": "Polished Maps: Cherry Temple",
        "notes": [
            "Polished Cherry Temple blooms as a lantern garden sanctuary.",
            "Petals drift around koi water and a ceremonial gate.",
        ],
        "details": [
            "Added Polished Cherry Temple with its protective life bonus intact.",
            "Preserved the original winding route and economy.",
            "Built a koi pond, flowering cherry trees, and shrine gateway.",
            "Added gently drifting blossom petals throughout the garden.",
            "Added a tiered shrine, arched bridge, lantern walk, and swimming koi.",
            "Added a tea pavilion, raked stone garden, bell, and bamboo fence.",
            "Changed the road into a ceremonial temple walk.",
            "Added a dedicated polished dictionary preview.",
        ],
    },
    {
        "version": "1.5.3",
        "title": "Polished Maps: Island Chain",
        "notes": [
            "Polished Island Chain becomes a moving tropical archipelago.",
            "Animated tides surround lush buildable islands.",
        ],
        "details": [
            "Added Polished Island Chain as a full ocean remaster.",
            "Preserved its route, high starting cash, and island-only placement.",
            "Built continuous blue water with animated surface wavelets.",
            "Added sandy green islands, palm details, and rising bubbles.",
            "Moved the northeastern island shoreline clear of the causeway.",
            "Changed the route into a rounded island causeway.",
            "Kept every original build island clearly visible.",
            "Added a dedicated polished dictionary preview.",
        ],
    },
    {
        "version": "1.5.2",
        "title": "Polished Maps: Mountain Pass",
        "notes": [
            "Polished Mountain Pass rises into an animated alpine valley.",
            "Snowy peaks, pines, and water now surround the tight route.",
        ],
        "details": [
            "Added Polished Mountain Pass as the third remastered battlefield.",
            "Preserved its tight-turn route, money, lives, and wave rewards.",
            "Built a continuous alpine valley beneath snow-capped peaks.",
            "Added evergreen stands, a glacial pool, and moving snow flecks.",
            "Added an animated waterfall, cliff lodge, and rope bridge.",
            "Added high circling birds and deeper layered mountain walls.",
            "Corrected the peak orientation so mountains rise upright.",
            "Changed the road into a weathered stone pass.",
            "Added a dedicated polished dictionary preview.",
        ],
    },
    {
        "version": "1.5.1",
        "title": "Polished Maps: Desert Ruins",
        "notes": [
            "Polished Desert Ruins joins the alternate collection.",
            "A living oasis and ancient temple replace the sand grid.",
        ],
        "details": [
            "Added Polished Desert Ruins as the second remastered battlefield.",
            "Kept the original Desert route, economy, lives, and build rules.",
            "Removed visible tile boundaries in favor of layered wind-carved dunes.",
            "Built a shimmering oasis basin with animated water ripples.",
            "Added swaying palm trees around the shaded water.",
            "Created a ruined sandstone temple with broken standing columns.",
            "Added a carved sun emblem and elevated ruin platform.",
            "Changed the route into a sunken sandstone causeway.",
            "Added worn slab markings, fractures, and obelisk route markers.",
            "Scattered cacti, broken pottery, and desert terrain props.",
            "Added moving heat shade, dune ridges, dust motes, and tumbleweed.",
            "Added a unique Desert Ruins preview in the Polished dictionary tab.",
        ],
    },
    {
        "version": "1.5.0",
        "title": "Polished Maps: Classic Meadow",
        "notes": [
            "Polished maps now live beside the classic collection.",
            "Classic Meadow is the first living, gridless battlefield.",
        ],
        "details": [
            "Started the Polished Maps release series with the original field.",
            "Added Classic and Polished tabs to map selection.",
            "Kept all ten original maps playable in the Classic collection.",
            "Added Polished Classic Meadow as a separate playable map.",
            "Preserved the original route, resources, lives, and placement rules.",
            "Removed visible square tiling from the polished battlefield.",
            "Painted continuous rolling grass and layered meadow clearings.",
            "Replaced square road cells with a rounded garden trail.",
            "Added cart tracks, cobbles, verge grass, and estate gate stones.",
            "Built an animated creek, wooden footbridge, and rippling lily pond.",
            "Added orchard trees, boundary fencing, and moving cloud shadows.",
            "Added dense swaying grasses and scattered flower details.",
            "Added drifting leaves and softly pulsing fireflies.",
            "Split the map dictionary into Classic and Polished tabs.",
            "Added a continuous painted preview for polished maps.",
            "Prepared the Polished tab for the remaining map remasters.",
        ],
    },
    {
        "version": "1.3.10",
        "title": "Special Overhaul: Starfall Prism",
        "notes": [
            "Starfall is now a celestial observatory prism.",
            "Selling a special correctly frees its one active slot.",
        ],
        "details": [
            "Completed the special-unit visual overhaul with Starfall Prism.",
            "Built an obsidian rooftop observatory with brass astrolabe rings.",
            "Suspended a luminous split-color prism over the instrument.",
            "Added turning orbit detail and small captured starlights.",
            "Changed its attacks into bright arcing five-point star shards.",
            "Created a matching pixel-art Ultra graphics model.",
            "Updated its dictionary description and home-screen showcase.",
            "Fixed shortcut selling so it resets the special placement slot.",
            "The battlefield now permits exactly one active special at a time.",
            "A sold special can be replaced with another special normally.",
        ],
    },
    {
        "version": "1.3.9",
        "title": "Special Overhaul: Guardian Gate",
        "notes": [
            "Guardian is now the Haunted Manor Gate.",
            "Place it on roads to stop passing enemies.",
        ],
        "details": [
            "Continued the special-unit overhaul with Guardian Gate.",
            "Remapped it as a wrought-iron haunted estate entrance.",
            "Added stone posts, pointed finials, braces, and a ghostly lock.",
            "Changed Guardian into a road-only placement special.",
            "Removed its ranged attack and former life-bonus role.",
            "Enemies reaching the gate are held for a fixed duration.",
            "Each enemy is held only once so waves eventually continue.",
            "Updated gameplay, special selection, preview, and Ultra models.",
            "Featured Haunted Manor Gate in the home-screen showcase.",
        ],
    },
    {
        "version": "1.3.8",
        "title": "Special Overhaul: Royal Mint",
        "notes": [
            "Royal Mint is now the Royal Coinworks.",
            "It mints bonus cash from enemies it defeats.",
        ],
        "details": [
            "Continued the special-unit overhaul with Royal Mint.",
            "Replaced its bank overlap with an industrial coin foundry.",
            "Built a brick workshop with a copper roof and chimney smoke.",
            "Added a glowing furnace window and turning press wheel.",
            "Added a coin chute with freshly stamped currency.",
            "Changed attacks into spinning golden coin projectiles.",
            "Removed its one-time placement payout identity.",
            "Added a difficulty-adjusted mint bounty for its own kills.",
            "Updated special selection, preview, and Ultra models.",
            "Featured Royal Coinworks in the home-screen showcase.",
        ],
    },
    {
        "version": "1.3.7",
        "title": "Special Overhaul: Thornheart",
        "notes": [
            "Thornheart is now a giant living bramble.",
            "It lashes enemies with a thorned vine tentacle.",
        ],
        "details": [
            "Continued the special-unit overhaul with Thornheart.",
            "Remapped it as the massive Thornheart Bramble.",
            "Built a dense spread of overlapping poisonous vines.",
            "Added hooked thorns and leafy growth around its silhouette.",
            "Placed a pulsing red heart inside the protected center.",
            "Changed attacks into writhing thorn-tentacle lashes.",
            "Moved each attack to emerge directly from the heart core.",
            "Preserved poison, splash damage, and its lives bonus.",
            "Updated gameplay, special selection, preview, and Ultra models.",
            "Featured Thornheart Bramble in the home-screen showcase.",
        ],
    },
    {
        "version": "1.3.6",
        "title": "Special Overhaul: Time Spire",
        "notes": [
            "Time Spire is now a giant working clock.",
            "Its hands display the real local time.",
        ],
        "details": [
            "Continued the special-unit overhaul with Time Spire.",
            "Remapped it as the monumental World Clock Spire.",
            "Built a stone-and-brass pedestal beneath a huge dial.",
            "Added hour markers, layered trim, and a glowing hub.",
            "Connected hour, minute, and second hands to system time.",
            "Updated the Ultra model with working clock hands too.",
            "Moved slowing attacks to originate at the clock center.",
            "Preserved its powerful group-control gameplay role.",
            "Updated special selection, previews, and home showcase.",
        ],
    },
    {
        "version": "1.3.5",
        "title": "Special Overhaul: Oracle",
        "notes": [
            "Oracle Lens is now a giant magnifying glass.",
            "Its focused glass projects long-range beams.",
        ],
        "details": [
            "Continued the special-unit overhaul with Oracle Lens.",
            "Remapped it as the oversized Grand Oracle Lens.",
            "Built an ornate display stand and long angled handle.",
            "Added a gold-violet rim around translucent blue glass.",
            "Painted bright reflective streaks across the lens face.",
            "Added a pulsing focal point within the magnifying glass.",
            "Moved beam attacks to originate at the focused lens point.",
            "Preserved its high-damage extreme-range targeting role.",
            "Updated gameplay, special selection, preview, and Ultra models.",
            "Featured Grand Oracle Lens in the home-screen showcase.",
        ],
    },
    {
        "version": "1.3.4",
        "title": "Direct Game Launch",
        "notes": [
            "The game can now launch from its own package.",
            "Main game file and module launch are supported.",
        ],
        "details": [
            "Added a direct launcher entrypoint inside tower_defense_game.",
            "The game now starts with python3 -m tower_defense_game.",
            "The main_game.py file can also be run directly.",
            "Kept test.py compatibility for existing launch habits.",
        ],
    },
    {
        "version": "1.3.3",
        "title": "Special Overhaul: Meteor",
        "notes": [
            "Meteor Beacon is now Meteor Volcano.",
            "It erupts arcing lava meteors at enemy groups.",
        ],
        "details": [
            "Continued the special-unit overhaul with Meteor Beacon.",
            "Remapped it as a compact active Meteor Volcano.",
            "Built a dark rocky cone with a glowing molten crater.",
            "Added bright lava fissures, smoke, and an erupting lava bomb.",
            "Changed projectiles into heavy molten meteor rocks.",
            "Added a dramatic high arc from the crater to each target.",
            "Added a landing flare for its broad splash impact.",
            "Preserved its slow, devastating group-damage role.",
            "Updated gameplay, special selection, preview, and Ultra models.",
            "Featured Meteor Volcano in the home-screen showcase.",
        ],
    },
    {
        "version": "1.3.2",
        "title": "Special Overhaul: Life Tree",
        "notes": [
            "Life Tree is now the Heart Orchard.",
            "Its glowing heart apples restore lives.",
        ],
        "details": [
            "Continued the special-unit overhaul with Life Tree.",
            "Remapped it as an ornate ancient Heart Orchard.",
            "Added a split carved trunk with curling exposed roots.",
            "Built a lush layered canopy with highlighted leaves.",
            "Hung three bright heart-shaped apples in the branches.",
            "Added subtle fruit shimmer for its healing identity.",
            "Preserved its one-time bonus of 8 additional lives.",
            "Updated gameplay, special selection, preview, and Ultra models.",
            "Featured the Heart Orchard in the home-screen showcase.",
        ],
    },
    {
        "version": "1.3.1",
        "title": "Special Overhaul: Treasury",
        "notes": [
            "Gold Vault is now the Pearl Treasury.",
            "A marble classical bank grants its funding bonus.",
        ],
        "details": [
            "Continued the special-unit overhaul with Gold Vault.",
            "Remapped it as the pearl-white Pearl Treasury bank.",
            "Built a wide marble staircase leading to the entry door.",
            "Added a classical facade with four bright pillars.",
            "Crowned the building with a Greco-Roman pediment.",
            "Placed a gold money crest above the front entrance.",
            "Preserved its one-time $260 funding bonus gameplay role.",
            "Updated gameplay, special selection, preview, and Ultra models.",
            "Featured the Pearl Treasury in the home-screen showcase.",
        ],
    },
    {
        "version": "1.3.0",
        "title": "Special Overhaul: Titan",
        "notes": [
            "The specials overhaul begins with Zeus Titan.",
            "Titan now hurls divine lightning from the clouds.",
        ],
        "details": [
            "Began the complete special-unit overhaul with Titan.",
            "Remapped Titan into a Zeus-inspired divine champion.",
            "Built a compact marble cloud pedestal beneath the figure.",
            "Added white-and-gold robes, a beard, and a golden crown.",
            "Raised one arm with a glowing lightning bolt in hand.",
            "Changed Titan projectiles from shells into lightning strikes.",
            "Moved attacks to discharge from the raised lightning bolt.",
            "Preserved Titan's devastating splash-damage gameplay role.",
            "Updated gameplay, special selection, preview, and Ultra models.",
            "Featured Zeus Titan in the home-screen showcase.",
        ],
    },
    {
        "version": "1.2.7",
        "title": "Storm Conductor",
        "notes": [
            "Storm is now a shrine trapping a thundercloud.",
            "Copper rods channel its slowing lightning.",
        ],
        "details": [
            "Remapped Storm as a compact elemental conductor shrine.",
            "Replaced the crystal silhouette with a low stone platform.",
            "Added three copper lightning rods with charged tips.",
            "Suspended a layered dark thundercloud over the rods.",
            "Animated a bright lightning channel inside the model.",
            "Moved lightning attacks up to discharge from the cloud.",
            "Updated gameplay, dictionary, preview, and Ultra models.",
            "Featured the remapped Storm in the home showcase.",
        ],
    },
    {
        "version": "1.2.6",
        "title": "Venom Canopy",
        "notes": [
            "Venom is now a snake hanging from a tree.",
            "Its leafy perch launches poison droplets.",
        ],
        "details": [
            "Remapped Venom as a compact jungle tree attacker.",
            "Replaced the crystal tower shape with a rooted trunk.",
            "Added branches and a layered leafy canopy.",
            "Draped a bright snake through the lower branch.",
            "Added an aimed snake head, eye blink, and forked tongue.",
            "Preserved poison-droplet attacks and damage over time.",
            "Updated gameplay, dictionary, preview, and Ultra models.",
            "Featured the remapped Venom in the home showcase.",
        ],
    },
    {
        "version": "1.2.5",
        "title": "Mortar Nest",
        "notes": [
            "Mortar is now a lightweight sandbag nest.",
            "A tripod tube launches its splash shells.",
        ],
        "details": [
            "Remapped Mortar as a compact indirect-fire position.",
            "Replaced the bulky body with a low sandbag crescent.",
            "Added a visible baseplate and three-legged support.",
            "Mounted a slim angled mortar tube in the firing pit.",
            "Placed spare shells beside the launcher for identity.",
            "Preserved high-arc shells and broad splash gameplay.",
            "Updated gameplay, dictionary, preview, and Ultra models.",
            "Featured the remapped Mortar in the home showcase.",
        ],
    },
    {
        "version": "1.2.4",
        "title": "Laser Grid Tower",
        "notes": [
            "Laser is now a steel power-line tower.",
            "A charged red orb emits its rapid beams.",
        ],
        "details": [
            "Remapped Laser as a compact transmission pylon.",
            "Built its structure from open steel lattice supports.",
            "Added crossarms and small power-line insulators.",
            "Mounted a pulsing red energy sphere at the tower top.",
            "Moved laser-beam origins up to the charged emitter orb.",
            "Layered red and white beam lines for a stronger shot.",
            "Updated gameplay, dictionary, preview, and Ultra models.",
            "Featured the remapped Laser in the home showcase.",
        ],
    },
    {
        "version": "1.2.3",
        "title": "Sniper Cliff Perch",
        "notes": [
            "Sniper now lies prone on a rocky cliff ledge.",
            "Sniper fires bullets; Arrow fires only one arrow.",
        ],
        "details": [
            "Remapped Sniper as a compact mountain-cliff emplacement.",
            "Added layered stone faces and a readable ledge edge.",
            "Placed the marksman prone along the firing shelf.",
            "Added a long rifle with a small muzzle glint.",
            "Updated gameplay, dictionary, preview, and Ultra models.",
            "Featured the remapped Sniper in the home showcase.",
            "Changed Sniper fire into a moving rifle bullet.",
            "Removed generic projectile glows from Sniper bullets.",
            "Removed generic projectile glows from Arrow shots.",
            "Removed extra Arrow hit particles so only one arrow flies.",
        ],
    },
    {
        "version": "1.2.2",
        "title": "Frost Wizard Tower",
        "notes": [
            "Frost is now a light-blue wizard tower.",
            "Arrow and Frost shots have distinct projectiles.",
        ],
        "details": [
            "Remapped Frost as a compact ice wizard tower.",
            "Added dimensional light-blue masonry and side facing.",
            "Added an open casting balcony with visible railing.",
            "Placed a frost wizard and glowing orb on the tower.",
            "Updated gameplay, dictionary, preview, and Ultra models.",
            "Featured the new Frost tower on the home screen.",
            "Changed Arrow fire into moving fletched arrows.",
            "Changed Frost fire into spinning snowflake shots.",
            "Added small ice crystals trailing snowflake attacks.",
        ],
    },
    {
        "version": "1.2.1",
        "title": "Cannon Field Kit",
        "notes": [
            "Cannon now uses a slimmer field emplacement.",
            "Fixed stacked towers drawing over Arrow lookouts.",
        ],
        "details": [
            "Remapped Cannon as the next compact troop model.",
            "Replaced its oversized body with a timber gun carriage.",
            "Added small wheels, an iron shield, and a short barrel.",
            "Kept the cannon shell identity and muzzle flash visible.",
            "Updated gameplay, dictionary, preview, and Ultra models.",
            "Added Cannon to the home-screen model showcase.",
            "Depth-sorted placed towers from background to foreground.",
            "Fixed upper-tile shadows hiding Arrow lookout details.",
        ],
    },
    {
        "version": "1.2.0",
        "title": "Troop Remap: Arrow",
        "notes": [
            "Arrow is now a wooden fire-lookout tower.",
            "The new 3D-style model appears in game and previews.",
        ],
        "details": [
            "Began the larger troop-remap series with the Arrow tower.",
            "Replaced the flat Arrow figure with a 3D-style lookout.",
            "Built the model around a compact wooden observation tower.",
            "Added open support legs so nearby units remain readable.",
            "Added wooden cross-bracing and a ladder below the deck.",
            "Added dimensional platform, cabin, roof, and window faces.",
            "Placed the ranger and bow on the elevated firing platform.",
            "Updated the Ultra pixel model to match the lookout tower.",
            "Updated dictionary inspection and showcase appearances.",
            "Featured the new Arrow lookout on the home screen.",
        ],
    },
    {
        "version": "1.1.4",
        "title": "Update Details",
        "notes": [
            "Release entries now open a detailed history view.",
            "Century updates can be browsed across pages.",
        ],
        "details": [
            "Made each visible home-screen release entry clickable.",
            "Added a dedicated release detail reader screen.",
            "Added previous and next paging for long release histories.",
            "Added keyboard paging with arrow keys and Back navigation.",
            "Loaded the full 100 QoL Century change descriptions.",
            "Loaded the full 100 Visual Finish Pass descriptions.",
        ],
    },
    {
        "version": "1.1.3",
        "title": "Visual Finish Pass",
        "notes": [
            "Added 100 small visual clarity and polish fixes.",
            "Refined menus, maps, combat feedback, models, and HUD.",
        ],
        "details": VISUAL_FINISH_DETAILS,
    },
    {
        "version": "1.1.2",
        "title": "QoL Century",
        "notes": [
            "Added 100 small control and clarity improvements.",
            "New stats, notices, HUD presets, and mouse actions.",
        ],
        "details": QOL_CENTURY_DETAILS,
    },
    {
        "version": "1.1.1",
        "title": "Difficulty Polish",
        "notes": [
            "Added difficulty previews, badges, and threat marks.",
            "Harder modes now send enemies more quickly.",
        ],
    },
    {
        "version": "1.1.0",
        "title": "Difficulty Modes",
        "notes": [
            "Added Easy, Medium, Hard, and Insane modes.",
            "Harder modes cut resources and strengthen waves.",
        ],
    },
    {
        "version": "1.0.7",
        "title": "Combat Tuning",
        "notes": [
            "Faster battles, larger enemies, and leaner rewards.",
            "Tower panel now tracks total damage.",
        ],
    },
    {
        "version": "1.0.6",
        "title": "Polish Pack",
        "notes": [
            "Added ten small visual and feedback upgrades.",
            "Improved placement, waves, combat, and UI clarity.",
        ],
    },
    {
        "version": "1.0.5",
        "title": "Tower Model Pass",
        "notes": [
            "Moved tower models into their own file.",
            "Rebuilt tower silhouettes and previews.",
        ],
    },
    {
        "version": "1.0.4",
        "title": "Fullscreen Polish",
        "notes": [
            "Added fullscreen toggle.",
            "Fixed map dictionary numbering.",
        ],
    },
    {
        "version": "1.0.3",
        "title": "Dictionary Models",
        "notes": [
            "Revamped dictionary previews.",
            "Animated inspection stage.",
        ],
    },
    {
        "version": "1.0.2",
        "title": "Tower Characters",
        "notes": [
            "Revamped tower models.",
            "Towers match their roles.",
        ],
    },
    {
        "version": "1.0.1",
        "title": "Special Showcase",
        "notes": [
            "3D special tower preview.",
            "Stats added to selector.",
        ],
    },
    {
        "version": "1.0.0",
        "title": "Full Release",
        "notes": [
            "Animated title screen.",
            "Tower and enemy showcase.",
        ],
    },
    {
        "version": "0.8.0",
        "title": "Folder Structure",
        "notes": [
            "Moved game into its own folder.",
            "Retro restored to grid style.",
        ],
    },
    {
        "version": "0.7.0",
        "title": "Update Log",
        "notes": [
            "Main-menu update history.",
            "Version numbers started.",
        ],
    },
    {
        "version": "0.6.0",
        "title": "Retro Revamp",
        "notes": [
            "Retro moved past tile graphics.",
            "Neon road and skyline.",
        ],
    },
    {
        "version": "0.5.1",
        "title": "Dictionary Upgrade",
        "notes": [
            "Maps and Characters sections.",
            "Rules and 3D previews.",
        ],
    },
    {
        "version": "0.5.0",
        "title": "Map Pack",
        "notes": [
            "Added 10 selectable maps.",
            "Map rules and rewards.",
        ],
    },
    {
        "version": "0.4.0",
        "title": "Upgrade Paths",
        "notes": [
            "Added two tower upgrade paths.",
            "Auto pause and menu return.",
        ],
    },
    {
        "version": "0.3.1",
        "title": "Graphics Pass",
        "notes": [
            "Higher-detail graphics modes.",
            "Hidden development tools.",
        ],
    },
    {
        "version": "0.3.0",
        "title": "Expanded Roster",
        "notes": [
            "More towers and enemies.",
            "Improved combat variety.",
        ],
    },
    {
        "version": "0.2.0",
        "title": "Menus",
        "notes": [
            "Start, settings, and dictionary.",
            "Volume and graphics settings.",
        ],
    },
    {
        "version": "0.1.0",
        "title": "First Playable",
        "notes": [
            "First tower defense loop.",
            "Waves, money, and lives.",
        ],
    },
]

EXPANDED_DETAILS = {
    "1.1.1": [
        "Added difficulty preview information before a match starts.",
        "Added difficulty badges and enemy threat markers in play.",
        "Made high-difficulty waves send enemies at a quicker pace.",
    ],
    "1.1.0": [
        "Added Easy, Medium, Hard, and Insane difficulty choices.",
        "Higher modes reduce tower damage and available resources.",
        "Higher modes increase enemy health, speed, and pressure.",
        "Higher modes reduce the lives available to defend.",
    ],
    "1.0.7": [
        "Increased battle pacing through faster tower attacks.",
        "Increased enemy size so incoming threats are easier to read.",
        "Reduced money gain to make building choices more meaningful.",
        "Added lifetime damage totals to the selected tower panel.",
        "Changed utility upgrades to improve speed and range.",
    ],
    "1.0.6": [
        "Added ten small combat and interface feedback improvements.",
        "Clarified tower placement and wave-state information.",
        "Improved presentation of attacks and battlefield actions.",
    ],
    "1.0.5": [
        "Moved tower model drawing into a dedicated module.",
        "Rebuilt towers as distinct readable role-based silhouettes.",
        "Updated tower previews to use the new model designs.",
    ],
    "1.0.4": [
        "Added fullscreen support and a settings toggle for it.",
        "Fixed numbering and selection behavior in the map dictionary.",
    ],
    "1.0.3": [
        "Revamped dictionary display screens for stronger previews.",
        "Added an animated inspection stage for viewed content.",
    ],
    "1.0.2": [
        "Replaced simple tower forms with character-like designs.",
        "Gave tower appearances readable identities for their roles.",
    ],
    "1.0.1": [
        "Added a showcase view for selecting the special tower.",
        "Added visible statistics to compare special choices.",
    ],
    "1.0.0": [
        "Added an animated title-screen battlefield scene.",
        "Added tower and enemy presentation on the home screen.",
        "Marked the initial full game release.",
    ],
    "0.8.0": [
        "Moved game source into the tower_defense_game package.",
        "Restored the Retro style to its intended grid presentation.",
    ],
    "0.7.0": [
        "Added release history to the main menu.",
        "Established displayed version numbers for future changes.",
    ],
    "0.6.0": [
        "Revamped the Retro visual mode beyond plain tile graphics.",
        "Added a neon road and skyline-inspired environment style.",
    ],
    "0.5.1": [
        "Expanded the dictionary into Maps and Characters sections.",
        "Added rule summaries and model previews for inspection.",
    ],
    "0.5.0": [
        "Added ten maps available for selection.",
        "Added per-map rules and reward differences.",
    ],
    "0.4.0": [
        "Added power and utility upgrade paths for towers.",
        "Added automatic pausing and a return-to-menu flow.",
    ],
    "0.3.1": [
        "Added higher-detail graphics mode options.",
        "Added hidden development tools for testing gameplay.",
    ],
    "0.3.0": [
        "Expanded the available tower roster.",
        "Expanded incoming enemy types.",
        "Improved variety across tower and enemy combat roles.",
    ],
    "0.2.0": [
        "Added start, settings, and dictionary menu screens.",
        "Added volume and graphics configuration options.",
    ],
    "0.1.0": [
        "Created the first playable tower-defense game loop.",
        "Added enemy waves, money rewards, and player lives.",
    ],
}

for update in UPDATE_LOG:
    if "details" not in update:
        update["details"] = EXPANDED_DETAILS[update["version"]]
