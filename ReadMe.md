# 🎨 Bézier Curve Visualizer with Pygame

This project visualizes a Bézier curve using Pygame. You can click and drag the red control points to dynamically reshape the curve in real-time.

---

## How It Works

The curve is generated using the explicit Bézier formula:

\[
B(t) = \sum_{i=0}^{n} \binom{n}{i} (1 - t)^{n-i} t^i P_i
\]

- `P_i` are control points (shown in red).
- Points connected with lines (100)

- Right click to create multiple Bezeir objects
- Select between Quadratic and Cubic curves

![me](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjJicTQ0bWpjaG85NDVhcHBpcWJiaTg5anNibXg3dXZweXVmMGVxMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/AjDlOPXjOGg49653n3/giphy.gif)
