/**
 * Core Competent - Dynamic Particle Network
 * Implements the "Neural Network" visual identity.
 */

class ParticleNetwork {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;

        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: null, y: null, radius: 150 }; // Interaction radius

        // Brand Colors
        this.colors = [
            '#DFA96C', // Warm Gold
            '#B8894A', // Muted Gold
            '#C9CDD1', // Cool Gray
            '#6B6F74'  // Mid Gray
        ];

        // Configuration
        this.config = {
            particleCount: window.innerWidth < 768 ? 40 : 80, // Fewer on mobile
            connectionDistance: 120,
            baseSpeed: 0.5,
            mouseRepel: false // Set true to repel, false to attract/connect
        };

        this.init();
    }

    init() {
        this.resize();
        this.createParticles();
        this.addEventListeners();
        this.animate();
    }

    resize() {
        this.canvas.width = this.canvas.parentElement.offsetWidth;
        this.canvas.height = this.canvas.parentElement.offsetHeight;

        // Adjust particle count on resize/orientation change
        this.config.particleCount = window.innerWidth < 768 ? 40 : 80;
        this.createParticles(); // Re-create to distribute evenly
    }

    createParticles() {
        this.particles = [];
        for (let i = 0; i < this.config.particleCount; i++) {
            const size = Math.random() * 2 + 1; // 1px to 3px
            const x = Math.random() * this.canvas.width;
            const y = Math.random() * this.canvas.height;
            const directionX = (Math.random() * 2) - 1; // -1 to 1
            const directionY = (Math.random() * 2) - 1;
            const color = this.colors[Math.floor(Math.random() * this.colors.length)];

            this.particles.push({
                x, y,
                vx: directionX * this.config.baseSpeed,
                vy: directionY * this.config.baseSpeed,
                size,
                color,
                originalX: x, // For potential spring-back effects
                originalY: y
            });
        }
    }

    addEventListeners() {
        window.addEventListener('resize', () => this.resize());

        // Mouse Move
        this.canvas.parentElement.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            this.mouse.x = e.clientX - rect.left;
            this.mouse.y = e.clientY - rect.top;
        });

        // Mouse Leave
        this.canvas.parentElement.addEventListener('mouseleave', () => {
            this.mouse.x = null;
            this.mouse.y = null;
        });
    }

    drawLines(p, i) {
        // Connect to other particles
        for (let j = i + 1; j < this.particles.length; j++) {
            const p2 = this.particles[j];
            const dx = p.x - p2.x;
            const dy = p.y - p2.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < this.config.connectionDistance) {
                const opacity = 1 - (distance / this.config.connectionDistance);
                this.ctx.strokeStyle = `rgba(198, 168, 124, ${opacity * 0.5})`; // Gold-ish tint
                this.ctx.lineWidth = 1;
                this.ctx.beginPath();
                this.ctx.moveTo(p.x, p.y);
                this.ctx.lineTo(p2.x, p2.y);
                this.ctx.stroke();
            }
        }

        // Connect to Mouse
        if (this.mouse.x !== null) {
            const dx = p.x - this.mouse.x;
            const dy = p.y - this.mouse.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < this.mouse.radius) {
                // Stronger connection to mouse
                const opacity = 1 - (distance / this.mouse.radius);
                this.ctx.strokeStyle = `rgba(223, 169, 108, ${opacity})`; // Warm Gold
                this.ctx.lineWidth = 1.5;
                this.ctx.beginPath();
                this.ctx.moveTo(p.x, p.y);
                this.ctx.lineTo(this.mouse.x, this.mouse.y);
                this.ctx.stroke();

                // Slight attraction to mouse (optional "Forming" effect)
                const forceDirectionX = dx / distance;
                const forceDirectionY = dy / distance;
                const force = (this.mouse.radius - distance) / this.mouse.radius;
                const attractionStrength = 0.05;

                // Move slightly towards mouse
                p.vx -= forceDirectionX * force * attractionStrength;
                p.vy -= forceDirectionY * force * attractionStrength;
            }
        }
    }

    update() {
        for (let i = 0; i < this.particles.length; i++) {
            let p = this.particles[i];

            // Movement
            p.x += p.vx;
            p.y += p.vy;

            // Boundary Check (bounce)
            if (p.x < 0 || p.x > this.canvas.width) p.vx = -p.vx;
            if (p.y < 0 || p.y > this.canvas.height) p.vy = -p.vy;

            // Speed Cap (since we modify velocity with mouse attraction)
            const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
            const maxSpeed = 2;
            if (speed > maxSpeed) {
                p.vx = (p.vx / speed) * maxSpeed;
                p.vy = (p.vy / speed) * maxSpeed;
            }

            // Draw Particle
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            this.ctx.fillStyle = p.color;
            this.ctx.fill();

            // Draw Connections
            this.drawLines(p, i);
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.update();
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    new ParticleNetwork('hero-canvas');
});
