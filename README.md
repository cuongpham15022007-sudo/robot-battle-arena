# Robot Battle Arena - Complete Edition

🤖 A 2D robot battle game inspired by Gundam-style mecha games with progression system, equipment, and multiple game modes!

## 🎮 Features

### Game Modes
- **PvP**: Two players battle it out in real-time
- **PvE**: Play against AI with 3 difficulty levels (Easy, Normal, Hard)
- **Main Menu**: Central hub for all game modes and features

### Robot Types (Unlock at different levels)
- **Warrior** (Level 1): Balanced stats with power strike ability
- **Assassin** (Level 5): Fast with high damage, dash attack ability
- **Tank** (Level 10): High HP and armor, shield ability
- **Mage** (Level 15): High attack power, fireball ability

### Progression System ⭐
- **Leveling**: Gain experience from battles
- **Gold Currency**: Earn gold to buy equipment
- **Robot Unlocking**: Unlock new robot types as you level up
- **Equipment System**: Buy and equip items to boost stats
- **Save/Load**: Progress is automatically saved to JSON file

### Equipment Shop 🛒
- **Weapons**: Increase attack power
  - Rusty Sword: +5 ATK (100 Gold)
  - Iron Sword: +10 ATK (250 Gold)
  - Steel Sword: +15 ATK (500 Gold)
  - Energy Sword: +25 ATK (1000 Gold)

- **Armor**: Increase armor/defense
  - Leather Armor: +10 ARM (100 Gold)
  - Iron Armor: +20 ARM (250 Gold)
  - Steel Armor: +30 ARM (500 Gold)
  - Legendary Armor: +50 ARM (1000 Gold)

- **Accessories**: Provide various stat bonuses
  - Health Ring: +50 HP (200 Gold)
  - Power Ring: +8 ATK (200 Gold)
  - Defense Ring: +15 ARM (200 Gold)
  - Crystal Orb: +100 HP +10 ATK +10 ARM (800 Gold)

### AI System
- **3 Difficulty Levels**: Easy, Normal, Hard
- **Adaptive Behavior**: AI adjusts strategy based on HP and distance
- **3 Play Styles**: Aggressive, Defensive, Balanced
- **Accuracy System**: Different accuracy based on difficulty

### Visual Effects ✨
- **Particle Effects**: Hit effects, heal effects, ability effects, level up effects
- **Floating Text**: Damage numbers, healing, level up notifications
- **Smooth Animations**: Particle trails, fading effects

### Save/Load System 💾
- **Player Profile Saving**: Progress is saved automatically to `player_stats.json`
- **Equipment Persistence**: Your equipped items are saved
- **Level & Gold Tracking**: All progression is persisted

## 📦 Installation

### Requirements
- Python 3.7+
- Pygame 2.5.2

### Setup

```bash
# Clone the repository
git clone https://github.com/cuongpham15022007-sudo/robot-battle-arena.git
cd robot-battle-arena

# Install dependencies
pip install -r requirements.txt

# Run the game
python game.py
```

## 🎮 Controls

### Battle Controls
**Player 1 (Red Robot)**
- **Movement**: W/A/S/D
- **Basic Attack**: SPACE
- **Special Ability**: LEFT SHIFT

**Player 2 (Blue Robot) - PvP Only**
- **Movement**: Arrow Keys (↑↓←→)
- **Basic Attack**: ENTER
- **Special Ability**: RIGHT CTRL

### Menu Navigation
- **Arrow Keys / Keyboard**: Navigate menus
- **ENTER / Click**: Confirm selection
- **ESC**: Go back

## 🎓 How to Play

1. **Start the game**: Launch `python game.py`
2. **Choose a mode**: 
   - Select "Start PvE" to play against AI
   - Select "Start PvP" to play with another player
3. **Select your robot**: Choose from unlocked robot types
4. **Battle**: Defeat your opponent to gain experience and gold
5. **Level up**: Unlock new robots and purchase equipment
6. **Visit the shop**: Buy equipment to boost your stats
7. **Check stats**: View your profile and progression

## 💪 Robot Abilities

### Warrior (Level 1)
- **Special Ability**: Power Strike (2x damage)
- **Stats**: 
  - HP: 150
  - Armor: 20
  - Attack: 15
  - Speed: 4
- **Best For**: Learning the game, balanced playstyle

### Assassin (Level 5)
- **Special Ability**: Dash Attack (Teleport + 1.5x damage)
- **Stats**:
  - HP: 80
  - Armor: 5
  - Attack: 25
  - Speed: 7
- **Best For**: Aggressive playstyle, hit-and-run tactics

### Tank (Level 10)
- **Special Ability**: Shield (Increase armor temporarily)
- **Stats**:
  - HP: 250
  - Armor: 40
  - Attack: 10
  - Speed: 2
- **Best For**: Defensive playstyle, absorbing damage

### Mage (Level 15)
- **Special Ability**: Fireball (2x AoE damage)
- **Stats**:
  - HP: 100
  - Armor: 10
  - Attack: 30
  - Speed: 5
- **Best For**: Ranged combat, high burst damage

## 📊 Leveling System

### Experience Rewards
- Victory: 200 EXP + (Level × 50) bonus EXP
- Gold Reward: 50% of EXP earned

### Level Progression
```
Level 1  → Start with Warrior
Level 5  → Unlock Assassin
Level 10 → Unlock Tank
Level 15 → Unlock Mage
Level 20+ → Master all robots!
```

### Experience Requirements
- Each level requires 15% more EXP than the previous level
- Starting EXP needed: 100
- Next level EXP: Current EXP × 1.15

### Level Benefits
- Increased battle rewards
- Unlock new robot types
- Equip better equipment
- More strategic options

## 🤖 AI Difficulty Levels

### Easy
- Longer decision intervals (2 seconds)
- Lower accuracy (60%)
- Slower reaction time
- Good for beginners

### Normal
- Balanced decision intervals (1 second)
- Medium accuracy (80%)
- Standard reaction time
- Recommended for most players

### Hard
- Quick decision intervals (0.5 seconds)
- High accuracy (95%)
- Fast reaction time
- Challenge for experienced players

## 🧠 AI Behavior

The AI makes strategic decisions based on:
- **Distance to player**: Determines when to attack, defend, or pursue
- **Current HP**: Low health triggers defensive mode
- **Robot type**: Uses abilities strategically
- **Difficulty level**: Affects accuracy and reaction time

### AI Strategies
1. **Aggressive Mode** (when enemy is close)
   - Uses special ability if available
   - Basic attacks on cooldown
   - Moves closer to enemy

2. **Defensive Mode** (when HP is low)
   - Keeps distance from enemy
   - Uses defensive abilities (Shield for Tank)
   - Moves away from danger

3. **Balanced Mode** (medium distance)
   - Approaches enemy carefully
   - Uses basic attacks when in range
   - Prepares for engagement

## 📁 Project Structure

```
robot-battle-arena/
├── game.py              # Main game logic with menus and battle system
├── robot.py             # Robot class with combat mechanics
├── ai_robot.py          # AI bot with strategic decision-making
├── progression.py       # Leveling, equipment, and player stats system
├── ui_menu.py          # Menu UI components (Main, Shop, Stats, Robot Select)
├── vfx.py              # Visual effects (particles and floating text)
├── requirements.txt     # Python dependencies
├── player_stats.json    # Auto-generated save file
└── README.md           # This file
```

## 🚀 Future Features

- [ ] 5v5 Team battles
- [ ] Campaign/Story mode
- [ ] More robot types (20+ total)
- [ ] Skill tree system
- [ ] Sound effects & music
- [ ] Multiple map varieties
- [ ] Ranked leaderboard
- [ ] Online multiplayer
- [ ] Robot customization/skins
- [ ] Special events & tournaments
- [ ] Item crafting system
- [ ] Quest system

## 🐛 Known Issues

- Particle effects may impact performance on older machines
- Equipment bonuses don't reset between battles (this is intentional!)
- AI may occasionally get stuck on screen edges

## 💡 Tips & Tricks

1. **Warrior is for beginners**: Learn the basics with balanced stats
2. **Tank vs Assassin**: Tanks counter Assassins with high defense
3. **Save gold for better equipment**: Early game equipment matters
4. **Level up multiple robots**: Different playstyles for different enemies
5. **Use abilities wisely**: Cooldowns are long, time them right!
6. **Buy equipment strategically**:
   - Weapon first for damage
   - Armor for defense
   - Accessories for versatility
7. **Equipment stacking**: You can equip Weapon + Armor + Accessory for maximum bonuses!

## 🎯 Strategy Guide

### Beginner Tips
1. Start with Warrior to learn basic combat
2. Focus on basic attacks until you learn cooldowns
3. Buy cheap equipment to test builds
4. Play Easy AI to learn patterns

### Intermediate Tips
1. Unlock Assassin for aggressive playstyle
2. Learn to time special abilities
3. Mix equipment for balanced stats
4. Play Normal AI for better challenge

### Advanced Tips
1. Master Tank for defensive gameplay
2. Use Mage for burst damage strategy
3. Combine equipment for specific builds
4. Play Hard AI for maximum challenge
5. Study AI patterns to predict moves

## 🤝 Contributing

Found a bug? Have an idea? Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📜 License

MIT License - Use this for learning, development, and fun!

## 👤 Author

Created by Cuong Pham (cuongpham15022007-sudo)

---

## 📈 Game Statistics

- **Robot Types**: 4 (with more planned)
- **Equipment Items**: 12 total
- **AI Difficulty Levels**: 3
- **Game Modes**: 2 (PvP + PvE)
- **Max Level**: Unlimited (scales exponentially)
- **Lines of Code**: 1000+

## 🎬 Getting Started Video Guide

1. Launch the game: `python game.py`
2. Click "Start PvE" or "Start PvP"
3. Select your robot type
4. Battle your opponent
5. Earn experience and gold
6. Visit the shop to buy equipment
7. Level up and unlock new robots
8. Repeat and dominate!

---

**Have fun dominating the arena!** 🤖⚔️🏆

**Created with ❤️ using Python & Pygame**

### Last Updated
- 2026-09-08: Complete progression system added
- Added: Leveling, Equipment, AI, VFX, Menus
- Status: Fully playable MVP (Minimum Viable Product)
