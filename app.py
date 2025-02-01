import streamlit as st
import streamlit.components.v1 as components

html_code = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Bouncing Yellow Balls in a Rotating Sphere</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.2/p5.js"></script>
  </head>
  <body>
    <script>
      // ----- Global Variables -----
      let balls = [];
      const numBalls = 15; // Using 15 balls instead of 100.
      const ballRadius = 10;
      let containerRadius;
      let rotationAngle = 0;

      // ----- Ball Class -----
      class Ball {
        constructor() {
          // Generate a random position inside the spherical container.
          let r = random(0, containerRadius - ballRadius);
          let theta = random(0, TWO_PI);
          let phi = random(0, PI);
          this.pos = createVector(
            r * sin(phi) * cos(theta),
            r * sin(phi) * sin(theta),
            r * cos(phi)
          );
          // Give the ball a random velocity in 3D.
          this.vel = createVector(random(-2, 2), random(-2, 2), random(-2, 2));
          this.radius = ballRadius;
        }
        
        update() {
          // Move the ball.
          this.pos.add(this.vel);
          
          // Check for collision with the spherical container.
          let d = this.pos.mag();
          if (d + this.radius > containerRadius) {
            let normal = this.pos.copy().normalize();
            // Reposition so the ball stays just inside the container.
            this.pos = normal.mult(containerRadius - this.radius);
            // Reflect the velocity: v' = v - 2*(v·n)*n.
            let dot = this.vel.dot(normal);
            this.vel.sub(normal.mult(2 * dot));
          }
        }
        
        display() {
          push();
          translate(this.pos.x, this.pos.y, this.pos.z);
          noStroke();
          fill(255, 255, 0); // Yellow color.
          sphere(this.radius);
          pop();
        }
      }

      // ----- p5.js Setup -----
      function setup() {
        createCanvas(windowWidth, windowHeight, WEBGL);
        // Set the container radius to 93% of the minimum canvas dimension.
        containerRadius = min(windowWidth, windowHeight) * 0.93 / 2;
        
        // Initialize the balls.
        for (let i = 0; i < numBalls; i++) {
          balls.push(new Ball());
        }
      }

      // ----- p5.js Draw Loop -----
      function draw() {
        background(30);  // Dark background.

        // Slowly update the rotation angle (scaled by 63%).
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
              // Collision detected.
              let n = delta.copy().normalize();
              let relVel = p5.Vector.sub(a.vel, b.vel);
              let speed = relVel.dot(n);
              if (speed < 0) {
                let impulse = n.copy().mult(-speed);
                a.vel.add(impulse);
                b.vel.sub(impulse);
              }
              // Separate overlapping balls.
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

      // Adjust canvas size on window resize.
      function windowResized() {
        resizeCanvas(windowWidth, windowHeight);
        containerRadius = min(windowWidth, windowHeight) * 0.93 / 2;
      }
    </script>
  </body>
</html>
"""

st.set_page_config(page_title="Bouncing Yellow Balls in Rotating Sphere")
st.title("Bouncing Yellow Balls in a Rotating Sphere")

components.html(html_code, height=600, scrolling=True)
