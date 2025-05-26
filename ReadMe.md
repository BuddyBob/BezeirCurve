# Bézier Curve Visualizer with Pygame

This project visualizes a Bézier curve using Pygame. You can click and drag the red control points to dynamically reshape the curve in real-time.

---

## How It Works

The curve is generated using the explicit Bézier formula:

\[
B(t) = \sum_{i=0}^{n} \binom{n}{i} (1 - t)^{n-i} t^i P_i
\]

- `P_i` are control points (shown in red).
- Points connected with lines (100)

## Features

- Right click to create multiple Bezeir objects
- Select between Quadratic and Cubic curves
- Click on tangent to visualize tangent lines at each point on curve
- Click and drag control points to reshape the curve
- Real-time updates as you drag control points
- See arc length of the curve

![me](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExN203cm9yd2V6bTY3Y3JncHdxdG90eWV6eTNqOXZ0MXo0Zjh0YzYzZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wlcdHrdepz51q4awfh/giphy.gif)
