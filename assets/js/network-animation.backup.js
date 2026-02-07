/**
 * Core Competent - Network Background Animation
 * Renders a subtle, interactive constellations/neural network effect.
 */

document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('network-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];

    // Configuration
    const particleCount = window.innerWidth > 768 ? 60 : 30; // Fewer particles on mobile
    const connectionDistance = 150;
    const mouseDistance = 200;

    // Resize handler
    function resize() {
        width = canvas.width = canvas.parentElement.offsetWidth;
        height = canvas.height = canvas.parentElement.offsetHeight;
    }

    window.addEventListener('resize', resize);
    resize();

    // Mouse tracking
    const mouse = { x: null, y: null };

    document.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        if (e.clientY >= rect.top && e.clientY <= rect.bottom) {
            mouse.x = e.clientX;
            mouse.y = e.clientY - rect.top; // Adjust for canvas position relative to viewport
        } else {
            mouse.x = null;
            mouse.y = null;
        }
    });

    document.addEventListener('mouseleave', () => {
        mouse.x = null;
        mouse.y = null;
    });

    // Particle Class
    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = (Math.random() - 0.5) * 0.5; // Very slow movement
            this.vy = (Math.random() - 0.5) * 0.5;
            this.size = Math.random() * 1.5 + 0.5;
            this.color = 'rgba(198, 168, 124, ' + (Math.random() * 0.3 + 0.1) + ')'; // Gold with varying opacity
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            // Bounce off edges
            if (this.x < 0 || this.x > width) this.vx *= -1;
            if (this.y < 0 || this.y > height) this.vy *= -1;

            // Mouse interaction (gentle repulsion)
            if (mouse.x != null) {
                let dx = mouse.x - this.x;
                let dy = mouse.y - this.y;
                let distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < mouseDistance) {
                    const forceDirectionX = dx / distance;
                    const forceDirectionY = dy / distance;
                    const force = (mouseDistance - distance) / mouseDistance;
                    const directionX = forceDirectionX * force * this.size * 0.5;
                    const directionY = forceDirectionY * force * this.size * 0.5;

                    this.vx -= directionX * 0.05;
                    this.vy -= directionY * 0.05;
                }
            }
        }

        draw() {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    // Initialize particles
    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }

    // Animation Loop
    function animate() {
        ctx.clearRect(0, 0, width, height);

        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();

            // Draw connections
            for (let j = i; j < particles.length; j++) {
                let dx = particles[i].x - particles[j].x;
                let dy = particles[i].y - particles[j].y;
                let distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < connectionDistance) {
                    ctx.beginPath();
                    // Opacity based on distance
                    let opacity = 1 - (distance / connectionDistance);
                    ctx.strokeStyle = 'rgba(198, 168, 124,' + (opacity * 0.15) + ')'; // Very subtle gold lines
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(animate);
    }

    animate();
});
