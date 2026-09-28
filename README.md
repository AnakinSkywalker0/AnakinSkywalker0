<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" width="880" alt="Abhishek Mishra — game development, systems design, real-time control">
</picture>

Real-time AI for games and robotics — boss behaviour, character controllers, and
control systems that turn a decision into motion within a frame budget. Unreal and
Unity, C++/C# for performance-critical code, Python for inference.

## CAT &nbsp;— Combat Adaptation Transformer

An adaptive boss AI stack for Unreal Engine. Local real-time inference reads player
behaviour and rewrites the boss's tactics mid-fight — instead of cycling scripted
phases, the encounter learns what you keep doing and counters it.

&nbsp;&nbsp;→ [Combat-Adaptation-Transformer](https://github.com/AnakinSkywalker0/Combat-Adaptation-Transformer) &nbsp;·&nbsp; `C++` `Unreal`

## Reflex Arc

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/arc-dark.svg">
  <img src="assets/arc-light.svg" width="880" alt="Reflex Arc: a language model reasons about the goal, a learned policy maps state to action, hardware executes the commands.">
</picture>

An LLM can plan but doesn't know what the hardware can physically do; a learned
policy is fast and precise but doesn't reason about goals. Reflex Arc pairs an
LLM planner with a trained control policy, running on a rover navigating a
classroom-sized Mars testbed.

I build the layer between them — translating plans into motor commands, and
keeping the rover moving if the connection drops.

&nbsp;&nbsp;→ [IshuIsAwake/reflex-arc](https://github.com/IshuIsAwake/reflex-arc) &nbsp;·&nbsp; `Python` `RL` `hardware`

## Smaller pieces

[**Dragon Arena Battle**](https://github.com/AnakinSkywalker0/DragonArenaBattle) — 2.5D
Unity arena, player vs. an FSM-driven dragon with fire, tail and flight attacks.
Two hours, start to polish.<br>
[**Node Based Dialogue System**](https://github.com/AnakinSkywalker0/NodeBasedDialogueSystem) — branching
dialogue authored on a graph, built on Unity's own GraphView API rather than a plugin.<br>
[**Morse Input**](https://github.com/AnakinSkywalker0/Morse_input_unity) — timing-detection
logic that reads Morse from key presses into game actions. `J` for jump.<br>
[**Emotiv EPOC X × Unity**](https://github.com/AnakinSkywalker0/Emotiv-Epoc-X-Unity-test-) — an
EEG headset wired into a Unity scene, to see what an unreliable input channel does
to game feel.

## Toolkit

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=unity,unreal,cpp,cs,py,blender&theme=dark">
  <img src="https://skillicons.dev/icons?i=unity,unreal,cpp,cs,py,blender&theme=light" alt="Unity, Unreal Engine, C++, C#, Python, Blender">
</picture>

<sub>+ real-time inference · reinforcement learning</sub>

---

<sub>[All repositories](https://github.com/AnakinSkywalker0?tab=repositories)</sub>
