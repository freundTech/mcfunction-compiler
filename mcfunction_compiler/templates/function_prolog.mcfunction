summon minecraft:armor_stand 0 0 0 {Marker: 1b, Invisible: 1b, NoGravity: 1b, Invulnerable: 1b, Tags: ["stack_frame"]}
scoreboard players add @e[type=armor_stand,tag="stack_frame"] mfc.stack_depth 1
