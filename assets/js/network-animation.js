/**
 * CORE COMPETENT - PREMIUM NETWORK ANIMATION
 * Estética: "Executive Deep Navy"
 * 
 * Un sistema de partículas performante que simula una constelación de datos
 * con movimiento de deriva (drift) fluido e interacción focal sutil.
 */

class NetworkAnimation {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;

        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.mouse = {
            x: null,
            y: null,
            active: false,
            influenceRadius: 150
        };

        // --- Critical Adjustable Variables ---
        this.config = {
            particleDensity: window.innerWidth / 150, // More divisor = more minimalist
            baseSpeed: 0.15,                           // Slow drift for premium feel
            connectionDistance: 180,                 // Threshold for inter-node lines
            mouseConnectionDistance: 200,            // Threshold for mouse focus
            particleColors: {
                standard: 'rgba(240, 246, 252, 0.3)', // Off-white subtle
                accent: 'rgba(198, 168, 124, 0.5)'    // Metallic Gold
            }
        };

        this.init();
    }

    init() {
        this.resize();
        this.createParticles();
        this.bindEvents();
        this.animate();
    }

    bindEvents() {
        // Debounced resize
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => this.resize(), 200);
        });

        // Mouse interaction
        window.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            this.mouse.x = e.clientX - rect.left;
            this.mouse.y = e.clientY - rect.top;
            this.mouse.active = true;
        });

        window.addEventListener('mouseleave', () => {
            this.mouse.active = false;
        });
    }

    resize() {
        this.width = this.canvas.width = this.canvas.parentElement.offsetWidth;
        this.height = this.canvas.height = this.canvas.parentElement.offsetHeight;

        // Re-calculate density on major resize
        if (this.particles.length > 0) {
            this.createParticles();
        }
    }

    createParticles() {
        this.particles = [];
        const count = Math.floor(this.config.particleDensity);

        for (let i = 0; i < count; i++) {
            const isAccent = Math.random() < 0.05; // 5% accent particles
            this.particles.push({
                x: Math.random() * this.width,
                y: Math.random() * this.height,
                vx: (Math.random() - 0.5) * this.config.baseSpeed,
                vy: (Math.random() - 0.5) * this.config.baseSpeed,
                size: Math.random() * 1.5 + 0.5,
                color: isAccent ? this.config.particleColors.accent : this.config.particleColors.standard
            });
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.width, this.height);

        for (let i = 0; i < this.particles.length; i++) {
            const p = this.particles[i];

            // Update position (Drift)
            p.x += p.vx;
            p.y += p.vy;

            // Fluid wrap-around
            if (p.x < 0) p.x = this.width;
            if (p.x > this.width) p.x = 0;
            if (p.y < 0) p.y = this.height;
            if (p.y > this.height) p.y = 0;

            // Mouse influence: Subtle focal point attraction
            if (this.mouse.active) {
                const dx = this.mouse.x - p.x;
                const dy = this.mouse.y - p.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < this.mouse.influenceRadius) {
                    const force = (this.mouse.influenceRadius - dist) / this.mouse.influenceRadius;
                    p.x += dx * force * 0.01;
                    p.y += dy * force * 0.01;

                    // Mouse connections
                    this.drawLink(p.x, p.y, this.mouse.x, this.mouse.y, dist, this.config.mouseConnectionDistance, true);
                }
            }

            // Draw Node
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            this.ctx.fillStyle = p.color;
            this.ctx.fill();

            // Inter-node connections
            for (let j = i + 1; j < this.particles.length; j++) {
                const p2 = this.particles[j];
                const dx = p.x - p2.x;
                const dy = p.y - p2.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < this.config.connectionDistance) {
                    this.drawLink(p.x, p.y, p2.x, p2.y, dist, this.config.connectionDistance, false);
                }
            }
        }

        requestAnimationFrame(() => this.animate());
    }

    drawLink(x1, y1, x2, y2, dist, threshold, isMouse) {
        const opacity = (1 - dist / threshold) * (isMouse ? 0.15 : 0.08);
        this.ctx.beginPath();
        this.ctx.moveTo(x1, y1);
        this.ctx.lineTo(x2, y2);
        this.ctx.strokeStyle = `rgba(255, 255, 255, ${opacity})`;
        this.ctx.lineWidth = isMouse ? 0.6 : 0.4;
        this.ctx.stroke();
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('hero-canvas')) {
        new NetworkAnimation('hero-canvas');
    }
});
