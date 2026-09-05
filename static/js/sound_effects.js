// ==============================================================================
// 手帳專屬觸感音效庫 (The Trace Handbook Procedural Sound FX)
// 使用 Web Audio API 即時程序化合成音效，無需額外下載音訊檔案，無延遲且輕量優雅。
// ==============================================================================

class JournalSoundFX {
    constructor() {
        this.ctx = null;
        this.enabled = localStorage.getItem('journal_sound_enabled') !== 'false'; // 預設開啟
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                this.ctx = new AudioContext();
            }
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    toggle() {
        this.enabled = !this.enabled;
        localStorage.setItem('journal_sound_enabled', this.enabled);
        if (this.enabled) {
            this.init();
            this.playChime();
        }
        return this.enabled;
    }

    // 1. 鋼筆在紙張上的輕微沙沙書寫聲 (Fountain Pen Scratch)
    playPenScratch() {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;

        try {
            const now = this.ctx.currentTime;
            // 雜訊緩衝區模擬紙張纖維磨擦
            const bufferSize = this.ctx.sampleRate * 0.04;
            const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.4));
            }

            const noise = this.ctx.createBufferSource();
            noise.buffer = buffer;

            const filter = this.ctx.createBiquadFilter();
            filter.type = 'bandpass';
            filter.frequency.value = 2200 + Math.random() * 800;
            filter.Q.value = 3.5;

            const gain = this.ctx.createGain();
            gain.gain.setValueAtTime(0.04, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);

            noise.connect(filter);
            filter.connect(gain);
            gain.connect(this.ctx.destination);

            noise.start(now);
        } catch (e) {}
    }

    // 2. 橡皮章按壓蓋印聲 (Rubber Stamp Thud)
    playStampThud() {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;

        try {
            const now = this.ctx.currentTime;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();

            osc.type = 'triangle';
            osc.frequency.setValueAtTime(140, now);
            osc.frequency.exponentialRampToValueAtTime(35, now + 0.12);

            gain.gain.setValueAtTime(0.35, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start(now);
            osc.stop(now + 0.13);
        } catch (e) {}
    }

    // 3. 手帳翻頁聲 (Page Turn Flip)
    playPageTurn() {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;

        try {
            const now = this.ctx.currentTime;
            const bufferSize = this.ctx.sampleRate * 0.14;
            const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                data[i] = (Math.random() * 2 - 1) * (1 - i / bufferSize);
            }

            const noise = this.ctx.createBufferSource();
            noise.buffer = buffer;

            const filter = this.ctx.createBiquadFilter();
            filter.type = 'lowpass';
            filter.frequency.setValueAtTime(1200, now);
            filter.frequency.linearRampToValueAtTime(400, now + 0.14);

            const gain = this.ctx.createGain();
            gain.gain.setValueAtTime(0.12, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.14);

            noise.connect(filter);
            filter.connect(gain);
            gain.connect(this.ctx.destination);

            noise.start(now);
        } catch (e) {}
    }

    // 4. 火漆烙印 / 沉澱完成溫潤風鈴音 (Warm Wooden / Ceramic Chime)
    playChime() {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;

        try {
            const now = this.ctx.currentTime;
            const freqs = [523.25, 659.25, 783.99]; // C5, E5, G5
            freqs.forEach((freq, idx) => {
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();

                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, now + idx * 0.07);

                gain.gain.setValueAtTime(0.08, now + idx * 0.07);
                gain.gain.exponentialRampToValueAtTime(0.0001, now + idx * 0.07 + 0.45);

                osc.connect(gain);
                gain.connect(this.ctx.destination);

                osc.start(now + idx * 0.07);
                osc.stop(now + idx * 0.07 + 0.48);
            });
        } catch (e) {}
    }
}

window.journalSFX = new JournalSoundFX();
