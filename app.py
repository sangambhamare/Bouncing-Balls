import streamlit as st
import streamlit.components.v1 as components

# The HTML code embeds a p5.js sketch.
html_code = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Bouncing Grey Balls in a Rotating Sphere</title>
    <!-- Include p5.js from a CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.2/p5.js"></script>
  </head>
  <body>
    <script>
      // ----- Global Variables -----
      let balls = [];
      const numBalls = 100;
      const ballRadius = 10;
      let containerRadius;
      let rotationAngle = 0;

      // ----- Ball Class -----
      class Ball {
        constructor() {
          // Generate a random position inside the sphere container.
          // We pick a random radius (up to containerRadius - ballRadius)
          // and random spherical angles.
          let r = random(0, containerRadius - ballRadius);
          let theta = random(0, TWO_PI);
          let phi = random(0, PI);
          this.pos = createVector(
            r * sin(phi) * cos(theta),
            r * sin(phi) * sin(theta),
            r * cos(phi)
          );
          // Give the ball a random velocity (in 3D)
          this.vel = createVector(random(-2, 2), random(-2, 2), random(-2, 2));
          this.radius = ballRadius;
        }
        
        update() {
          // Move the ball
          this.pos.add(this.vel);
          
          // Check collision with the spherical container.
          // If the ball’s outer edge is outside the container, reflect its velocity.
          let d = this.pos.mag();
          if (d + this.radius > containerRadius) {
            let normal = this.pos.copy().normalize();
            // Reposition so it stays just inside the container.
            this.pos = normal.mult(containerRadius - this.radius);
            // Reflect the velocity: v' = v - 2*(v·n)*n
            let dot = this.vel.dot(normal);
            this.vel.sub(normal.mult(2 * dot));
          }
        }
        
        display() {
          push();
          translate(this.pos.x, this.pos.y, this.pos.z);
          noStroke();
          fill(150);  // Grey color for the ball.
          sphere(this.radius);
          pop();
        }
      }

      // ----- p5.js Setup -----
      function setup() {
        createCanvas(windowWidth, windowHeight, WEBGL);
        // Set the container radius to 93% of the minimum canvas dimension
        containerRadius = min(windowWidth, windowHeight) * 0.93 / 2;
        
        // Initialize the balls.
        for (let i = 0; i < numBalls; i++) {
          balls.push(new Ball());
        }
      }

      // ----- p5.js Draw Loop -----
      function draw() {
        background(30);  // Dark background

        // Slowly update the rotation angle.
        // The "63% factor" is applied here to slow down the rotation.
        rotationAngle += 0.005 * 0.63;
        rotateY(rotationAngle);
        rotateX(rotationAngle / 2);
        
        // Draw the container sphere as a wireframe.
        noFill();
        stroke(255);
        strokeWeight(1);
        sphere(containerRadius);

        // Update positions for each ball.
        for (let i = 0; i < numBalls; i++) {
          balls[i].update();
        }
        
        // --- Ball-to-Ball Collision Detection & Response ---
        for (let i = 0; i < numBalls; i++) {
          for (let j = i + 1; j < numBalls; j++) {
            let a = balls[i];
            let b = balls[j];
            let delta = p5.Vector.sub(a.pos, b.pos);
            let dist = delta.mag();
            if (dist < a.radius + b.radius) {
              // A collision is detected.
              let n = delta.copy().normalize();
              // Determine relative velocity along the normal.
              let relVel = p5.Vector.sub(a.vel, b.vel);
              let speed = relVel.dot(n);
              if (speed < 0) {
                // For equal masses in an elastic collision, swap the normal components.
                let impulse = n.copy().mult(-speed);
                a.vel.add(impulse);
                b.vel.sub(impulse);
              }
              // Separate overlapping balls to avoid sticking.
              let overlap = a.radius + b.radius - dist;
              let separation = n.copy().mult(overlap / 2);
              a.pos.add(separation);
              b.pos.sub(separation);
            }
          }
        }
        
        // Display all balls.
        for (let i = 0; i < numBalls; i++) {
          balls[i].display();
        }
      }

      // Resize the canvas if the window size changes.
      function windowResized() {
        resizeCanvas(windowWidth, windowHeight);
        containerRadius = min(windowWidth, windowHeight) * 0.93 / 2;
      }
    </script>
  </body>
</html>
"""

# ----- Streamlit App Configuration -----
st.set_page_config(page_title="Bouncing Grey Balls in Rotating Sphere")
st.title("Bouncing Grey Balls in a Rotating Sphere")

st.markdown(
    """
This demo uses a p5.js sketch embedded inside a Streamlit app.  
The scene consists of 100 grey balls bouncing elastically inside a spherical container whose size is 93% of the canvas,  
with the whole sphere slowly rotating (using a 63% scaling on the rotation speed).
"""
)

# Embed the p5.js sketch.
components.html(html_code, height=600, scrolling=True)
