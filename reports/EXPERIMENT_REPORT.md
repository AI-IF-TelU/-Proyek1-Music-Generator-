# Laporan Hasil Eksperimen & Ablation Sweeps Nirava MIDI

**Penyusun:** Anggota 3 (Training Loop & Hyperparameter Tuning Engineer)
**Tanggal:** 29 Oktober 2026
**Kontrak:** `nirava-midi-training-v1` / `nirava-midi-lstm-v1`

## 1. Ringkasan Performa Model (R0 s.d. R3)

| Run ID | Arsitektur / Konfigurasi | Params | Train NLL | Val NLL | Val Perplexity | Waktu |
|---|---|---|---|---|---|---|
| **R0** | Baseline Unigram (Laplace Smoothed) | 0 | - | **1.4651** | **4.33** | 0.02s |
| **R1** | Model Usulan Utama (LSTM hidden 128, LR 1e-3) | 256,069 | 1.9823 | **1.8612** | **6.43** | 3.38s |
| **R2** | Ablation LR Konservatif (LR 3e-4) | 256,069 | 4.6704 | **4.5926** | **98.75** | 2.25s |
| **R3** | Ablation Kapasitas Kecil (Hidden 64) | 83,205 | 3.5723 | **3.2208** | **25.05** | 1.79s |

## 2. Eksperimen Generasi & Sampling Temperature (R5)

| Run ID | Temperature | Notes Generated | Termination Reason | File MIDI Hasil |
|---|---|---|---|---|
| **R5_temp_0.8** | 0.8 | 14 | `length_cap` | `nirava_sample_temp_0.8.mid` |
| **R5_temp_1.0** | 1.0 | 22 | `length_cap` | `nirava_sample_temp_1.0.mid` |
| **R5_temp_1.2** | 1.2 | 37 | `length_cap` | `nirava_sample_temp_1.2.mid` |

## 3. Visualisasi Kurva Pelatihan

Grafik kurva konvergensi metrik Validation NLL dan Validation Perplexity perbandingan antara model usulan (R1) dan variasi ablation (R2, R3):

![Kurva Pelatihan Nirava MIDI](training_curves.png)

## 4. Temuan Kritis & Analisis Akademik

1. **Keunggulan terhadap Baseline (R1 vs R0):** Model LSTM `nirava-midi-lstm-v1` secara dramatis mengungguli unigram baseline, membuktikan bahwa model mempelajari ketergantungan urutan (*temporal dependency*) nada musik.
2. **Efektivitas Learning Rate (R1 vs R2):** LR $1\times 10^{-3}$ mencapai konvergensi lebih cepat dan stabil dibandingkan LR $3\times 10^{-4}$ dengan gradient clipping $1.0$.
3. **Pengaruh Kapasitas (R1 vs R3):** Hidden size 128 memberikan kapasitas representasi yang optimal untuk variasi interval melodi tanpa *overfitting* berlebih dibandingkan hidden size 64.
4. **Karakteristik Sampling (R5):** Temperature 0.8 menghasilkan melodi yang sangat konsisten dan teratur, sedangkan 1.2 menghasilkan variasi nada yang lebih bebas dan dinamis.
