# 👽 Little Grey Adventure

> An **endless runner** developed with **Python + Pygame**, featuring original pixel art and a focus on scalable game systems.

---

## 🎬 Preview

![Gameplay](gameplay.gif)

---

## 🎮 Play the game

https://danigator.itch.io/little-grey-adventure

---

## 🎮 Gameplay

* 🏃 Continuous automatic movement
* ⬆️ **Jump** to avoid obstacles
* ⬇️ **Duck** to dodge low enemies
* 💀 Dynamic obstacles: rocks and creatures
* 📈 Progressive **score system**
* 🧠 Challenge yourself to beat your **high score**

---

## ✨ Highlights

* 🎨 **Original pixel art** (character, enemies, environment)
* ⚙️ Modular and scalable architecture
* 🔁 Endless gameplay with progressive difficulty
* 🎬 Smooth animations (run cycle + states)
* 💥 Visual feedback:

  * Jump particles
  * Screen shake
* 🌍 Continuous world simulation (moving ground)
* 🎯 Procedural obstacle spawn system

---

## 🧠 Architecture & Systems

The project is structured into decoupled systems to ensure scalability and maintainability:

### 🧍 Player System

* Player configuration
* Enhanced jump system (**jump tuning**)
* Duck mechanic
* Animations (idle/run/jump)
* Particle system

### 🧱 Obstacle System

* Sprite loading and management
* Dynamic obstacle generation
* Pattern-based spawn system

### 🎮 Game State System

* States: `Playing`, `Game Over`
* Clean state transitions
* Game restart logic

### 📈 Score System

* Real-time score tracking
* Persistent **high score**

### 🔁 Core Loop

* Optimized game loop
* Event handling
* Logic/render separation

### 🎨 Visual Systems

* Animations
* Screen shake
* Ground movement
* Player feedback systems

---

## 🔄 Game Flow

1. Start in **Playing** state
2. Obstacles spawn progressively
3. Player reacts with jump / duck
4. Difficulty increases over time
5. Collision → **Game Over**
6. High score is recorded
7. Instant restart

---

## ⚙️ Installation

```bash id="y0bdhb"
pip install pygame
```

---

## ▶️ Run the Game

```bash id="zvjd83"
python main.py
```

---

## 🧾 Technical Notes

* The game uses a classic **game loop** with separated logic and rendering.
* Difficulty scales progressively through a **dynamic obstacle spawn system**.
* Movement mechanics (jump & duck) are tuned for responsive **game feel**.
* Animations are handled via **spritesheets** and state-based logic.
* Visual feedback includes **screen shake** and particle effects.
* The architecture is modular, allowing easy expansion and maintenance.

---

## 💡 Design Notes

* The main goal was to create a simple yet addictive experience based on **reflexes and timing**.
* The duck mechanic adds an extra layer of decision-making.
* The pixel art style aims for a retro feel with a unique identity.
* The pacing is designed to gradually increase tension.

---

## 🛠️ Developer Notes

* This project was built as a **game development practice** using Pygame.
* All art assets were created manually in pixel art style.
* One of the biggest challenges was refining the **jump feel** and responsiveness.
* The obstacle system was designed to be scalable and easily configurable.

---

## 🚀 Key Learnings

* Real-time **game loop design**
* Game state management
* Animation systems in Pygame
* Modular architecture and separation of concerns
* Implementing **visual feedback** for better UX
* Basic procedural generation techniques

---

## 🔮 Future Improvements

* 🔊 Sound effects and music
* 🎮 Gamepad support
* 🧠 Enemy AI
* 🌐 Online leaderboard
* ⚡ Power-ups

---

## 👨‍🎨 Author

Developed and illustrated by me as a personal project.
Focused on improving skills in **game development** and system design.

---

📝 License
CC - BY - NC - SA


