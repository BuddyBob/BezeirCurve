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

## Features

- Right click to create multiple Bezeir objects
- Select between Quadratic and Cubic curves
- Click on tangent to visualize tangent lines at each point on curve
- Click and drag control points to reshape the curve
- Real-time updates as you drag control points
- Visualize tangent lines at each point on the curve
- Visualize acceleration at each poiint on curve
- See arc length of the curve

![me](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHBtcnF5MnM0aHBvdGxtenl6Z3phZTV6Y3IyczQzODJoc2wyNTMzcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/4yCbf4BKETAZLB4lGt/giphy.gif)
