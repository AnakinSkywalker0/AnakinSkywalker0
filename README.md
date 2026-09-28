<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" width="880" alt="Abhishek Mishra — game development, systems design, real-time control">
</picture>

I build things that have to move before they can be right. Most of my work sits in
one seam: a system decides something, and a body — a boss, a rover, a character
controller — has to do it inside a frame. Unreal and Unity, C++ and C# when the
budget is tight, Python when the thing has to think.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cat-dark.svg">
  <img src="assets/cat-light.svg" width="880" alt="CAT — Combat Adaptation Transformer: adaptive boss AI for Unreal Engine">
</picture>

An adaptive boss AI stack for Unreal Engine. It runs local real-time inference to
read player behaviour, detect combat patterns, and rewrite the boss's tactics
mid-fight. Instead of cycling scripted phases, the encounter learns what you keep
doing and starts countering it.

&nbsp;&nbsp;→ [Combat-Adaptation-Transformer](https://github.com/AnakinSkywalker0/Combat-Adaptation-Transformer) &nbsp;·&nbsp; `C++` `Unreal`

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/arc-dark.svg">
  <img src="assets/arc-light.svg" width="880" alt="Reflex Arc: a language model decides, a learned policy acts, hardware executes.">
</picture>

A language model can reason about what ought to be done and has no idea what the
body it is driving can physically do. A learned policy has the opposite deficit —
precise, reactive, fast, and with no opinion about which coordinate matters. Reflex
Arc stacks them so neither has to be the other, and points the result at a rover
crossing a classroom-sized Mars.

I work the seam in the middle: the bridge that turns the planner's intent into motor
commands, and keeps the rover driving when the network stalls.

&nbsp;&nbsp;→ [IshuIsAwake/reflex-arc](https://github.com/IshuIsAwake/reflex-arc) &nbsp;·&nbsp; `Python` `RL` `hardware`

## Smaller pieces

[**Dragon Arena Battle**](https://github.com/AnakinSkywalker0/DragonArenaBattle) — a 2.5D
arena in Unity 6.3, player against an FSM-driven dragon with fire, tail and flight.
Two hours, start to polish, kept as a clean record of how it was built.<br>
[**Node Based Dialogue System**](https://github.com/AnakinSkywalker0/NodeBasedDialogueSystem) — branching
dialogue authored on a graph, built on Unity's own GraphView API rather than a plugin.<br>
[**Morse Input**](https://github.com/AnakinSkywalker0/Morse_input_unity) — timing-detection
logic that reads Morse from key presses and maps it onto game actions. `J` for jump.<br>
[**Emotiv EPOC X × Unity**](https://github.com/AnakinSkywalker0/Emotiv-Epoc-X-Unity-test-) — an
EEG headset wired into a Unity scene, to find out what an unreliable input channel
does to game feel.

## Toolkit

```
engines    Unreal · Unity
languages  C++ · C# · Python
adjacent   Blender · real-time inference · reinforcement learning
```

---

<sub>[All repositories](https://github.com/AnakinSkywalker0?tab=repositories)</sub>
