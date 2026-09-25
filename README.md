# Boids Flocking Simulation

An implementation of Craig Reynolds' classic artificial life algorithm (1986), simulating the emergent flocking dynamics of birds, schools of fish, and swarms. The project includes physical wall collision bouncing and real-time interactive predator avoidance, available both as a web-based Canvas simulation and as a native desktop application using Pygame.

---

## Overview

The Boids model demonstrates how complex, realistic group behavior emerges from individuals following three simple local steering rules without any centralized coordination:

1. **Separation:** Steer to avoid crowding or colliding with nearby flockmates.
2. **Alignment:** Steer to match the average velocity and heading of neighboring flockmates.
3. **Cohesion:** Steer towards the average position (center of mass) of local flockmates.

In addition to standard flocking dynamics, this repository introduces:

* **Physical Bounce Boundaries:** Rather than wrapping across edges (toroidal topology), boids reflect their velocity vectors when hitting boundary limits, preserving spatial containment.
* **Dynamic Predator Avoidance:** The cursor (or touch input) functions as a dynamic apex predator. Boids actively flee when within the danger zone, and the predator dynamically faces its direction of movement.

---

## Repository Structure

```
boids/
|-- index.html     # Web-based interactive simulation (HTML5 Canvas + JavaScript)
|-- main.py        # Desktop 2D simulation built with Pygame
|-- server.py      # Lightweight local HTTP server for hosting index.html
\-- README.md      # Project documentation
```

---

## Features

* **Dual Implementations:**
  * **Web Application (`index.html`):** Hardware-accelerated HTML5 Canvas with smooth responsive scaling, real-time FPS counter, neon glowing aesthetic, and mobile touch support.
  * **Desktop Application (`main.py`):** Native Python simulation rendered via `pygame` at a fixed 60 FPS update rate.
* **Interactive Parameters:**
  * Real-time boid count slider to test flock density and performance scaling.
  * Automatic scaling of boid density on small screen viewports.
* **Dynamic Vector Mathematics:**
  * Euclidean distance calculations for local neighborhood querying.
  * Reynolds steering force formulation: `steering = desired_velocity - current_velocity`, clamped to maximum force thresholds.

---

## Simulation Mechanics

### 1. Steering Rules

* **Separation:**
  Each boid calculates a repulsive force from neighbors within a defined threshold (`DESIRED_SEPARATION = 30px`), inversely proportional to distance:
  $$\vec{F}_{sep} = \sum \frac{\vec{pos}_{self} - \vec{pos}_{other}}{|\vec{pos}_{self} - \vec{pos}_{other}|}$$

* **Cohesion:**
  Each boid computes the center of mass of neighbors within its perception radius (`PERCEPTION_RADIUS = 100px`) and applies a steering vector towards that point:
  $$\vec{center} = \frac{1}{N} \sum \vec{pos}_{other}, \quad \vec{desired} = \text{normalize}(\vec{center} - \vec{pos}_{self}) \cdot v_{max}$$

* **Alignment:**
  Each boid computes the mean velocity of neighboring boids within its perception radius and steers towards that velocity:
  $$\vec{v}_{avg} = \frac{1}{N} \sum \vec{v}_{other}, \quad \vec{steering} = \vec{v}_{avg} - \vec{v}_{self}$$

### 2. Boundary Reflections

When a boid reaches the boundary of the canvas or display window:
* Left/Right walls: `vx = -vx`
* Top/Bottom walls: `vy = -vy`
Position is clamped to the edge to prevent clipping outside the viewable area.

### 3. Predator Avoidance

The cursor is tracked as a predator:
* When the distance between a boid and the cursor drops below 80 pixels, an evasion vector pointing directly away from the predator is scaled to twice the normal maximum speed and applied as an evasive steering force.
* The predator graphic dynamically rotates to match its direction of travel.

---

## Getting Started

### Prerequisites

* Python 3.8 or higher
* A modern web browser (Chrome, Firefox, Safari, Edge)
* (Optional) `pygame` library if running the desktop application

---

### Running the Web Simulation Locally

You can run the web simulation using the included HTTP server:

1. Launch the local server:
   ```bash
   python server.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

Alternatively, open `index.html` directly in any web browser.

---

### Running the Desktop Python Simulation

1. Install Pygame if not already installed:
   ```bash
   pip install pygame
   ```

2. Run the simulation:
   ```bash
   python main.py
   ```

3. Interaction:
   * Move the mouse across the simulation window to guide the predator.
   * Close the window or press Alt+F4 to exit.

---

## Configuration Reference

Both implementations use consistent physical parameters that can be adjusted in the source code:

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| `WIDTH` | 1000 | Canvas / display width in pixels |
| `HEIGHT` | 800 | Canvas / display height in pixels |
| `BOID_COUNT` | 100 | Default number of boids in the simulation |
| `PERCEPTION_RADIUS` | 100 | Radius in pixels within which boids detect neighbors |
| `DESIRED_SEPARATION` | 30 | Minimum distance boids maintain from each other |
| `MAX_SPEED` | 2.5 (web) / 4.0 (py) | Maximum velocity magnitude for a boid |
| `MAX_FORCE` | 0.1 | Maximum steering force applied per frame |
| Avoidance Radius | 80 | Distance threshold for fleeing the predator |

---

## Technical Highlights

* **Zero External Web Dependencies:** The web application is implemented in pure HTML5 and vanilla JavaScript without external libraries or frameworks.
* **Efficient Canvas Rendering:** Employs requestAnimationFrame with dirty clearing and procedural path drawing to maintain stable 60 FPS execution on modern hardware.
* **Cross-Platform Server Script:** `server.py` is configured with UTF-8 console output handling and automatic browser launching for Windows, macOS, and Linux environments.

---

## References

* Reynolds, C. W. (1987). Flocks, herds and schools: A distributed behavioral model. *ACM SIGGRAPH Computer Graphics*, 21(4), 25-34.
