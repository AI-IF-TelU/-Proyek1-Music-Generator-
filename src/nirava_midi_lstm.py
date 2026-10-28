"""Arsitektur model nirava-midi-lstm-v1 (from scratch PyTorch autograd).

Sesuai docs/ML_ARCHITECTURE.md:
- Vocabulary V=133
- Embedding E=64
- 2 layer LSTM unidirectional manual (NiravaLSTMCell) hidden=128
- Linear projection head: 128 -> 133 logits
- Inisialisasi: forget gate bias = 1.0, bias lain = 0.0
- Tidak menggunakan pretrained weights/embeddings.
"""

import math
import torch
import torch.nn as nn

MODEL_VERSION = "nirava-midi-lstm-v1"
VOCAB_SIZE = 133
EMBEDDING_DIM = 64
HIDDEN_DIM = 128
NUM_LAYERS = 2


class NiravaLSTMCell(nn.Module):
    """Satu sel LSTM yang dibangun dari operasi dasar PyTorch tensor dan Linear.

    Persamaan:
      a_t = W_x * x_t + W_h * h_prev + b
      i_t, f_t, g_t, o_t = split(a_t)
      i_t = sigmoid(i_t)
      f_t = sigmoid(f_t)
      g_t = tanh(g_t)
      o_t = sigmoid(o_t)
      c_t = f_t * c_prev + i_t * g_t
      h_t = o_t * tanh(c_t)
    """

    def __init__(self, input_dim: int, hidden_dim: int):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim

        # Matriks bobot transformasi input x dan hidden h: [4 * hidden_dim, dim]
        self.w_ih = nn.Linear(input_dim, 4 * hidden_dim, bias=True)
        self.w_hh = nn.Linear(hidden_dim, 4 * hidden_dim, bias=False)

        self.reset_parameters()

    def reset_parameters(self):
        """Inisialisasi bobot standard uniform dan forget gate bias = 1.0."""
        std = 1.0 / math.sqrt(self.hidden_dim)
        nn.init.uniform_(self.w_ih.weight, -std, std)
        nn.init.uniform_(self.w_hh.weight, -std, std)
        nn.init.zeros_(self.w_ih.bias)

        # Inisialisasi forget gate bias = 1.0 untuk mencegah vanishing gradient di awal training
        with torch.no_grad():
            # Urutan gerbang: i, f, g, o
            # f berada di indeks [hidden_dim : 2 * hidden_dim]
            self.w_ih.bias[self.hidden_dim:2 * self.hidden_dim].fill_(1.0)

    def forward(self, x_t: torch.Tensor, h_prev: torch.Tensor, c_prev: torch.Tensor):
        """Forward satu time step.

        Args:
            x_t: [B, input_dim]
            h_prev: [B, hidden_dim]
            c_prev: [B, hidden_dim]

        Returns:
            h_t: [B, hidden_dim]
            c_t: [B, hidden_dim]
        """
        gates = self.w_ih(x_t) + self.w_hh(h_prev)  # [B, 4 * hidden_dim]
        i_gate, f_gate, g_gate, o_gate = gates.chunk(4, dim=-1)

        i_t = torch.sigmoid(i_gate)
        f_t = torch.sigmoid(f_gate)
        g_t = torch.tanh(g_gate)
        o_t = torch.sigmoid(o_gate)

        c_t = f_t * c_prev + i_t * g_t
        h_t = o_t * torch.tanh(c_t)

        return h_t, c_t


class NiravaLSTMLanguageModel(nn.Module):
    """Model bahasa autoregresif untuk sequence token MIDI nirava-midi-lstm-v1.

    Arsitektur:
      Token IDs [B, T] -> Embedding(133, 64) -> LSTM Layer 1 (64 -> 128)
      -> LSTM Layer 2 (128 -> 128) -> Linear Head (128 -> 133) -> Logits [B, T, 133].
    """

    def __init__(
        self,
        vocab_size: int = VOCAB_SIZE,
        embedding_dim: int = EMBEDDING_DIM,
        hidden_dim: int = HIDDEN_DIM,
        num_layers: int = NUM_LAYERS,
    ):
        super().__init__()
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        # Learned embedding dari inisialisasi acak
        self.embedding = nn.Embedding(vocab_size, embedding_dim)

        # Dua lapis LSTM cells
        self.cell_layer1 = NiravaLSTMCell(embedding_dim, hidden_dim)
        self.cell_layer2 = NiravaLSTMCell(hidden_dim, hidden_dim)

        # Linear projection head ke seluruh vocabulary
        self.head = nn.Linear(hidden_dim, vocab_size)

        self.reset_parameters()

    def reset_parameters(self):
        """Inisialisasi embedding dan projection head."""
        nn.init.normal_(self.embedding.weight, mean=0.0, std=0.02)
        nn.init.xavier_uniform_(self.head.weight)
        nn.init.zeros_(self.head.bias)
        self.cell_layer1.reset_parameters()
        self.cell_layer2.reset_parameters()

    def init_hidden(self, batch_size: int, device: torch.device = None):
        """Buat state (h0, c0) bernilai 0 dengan bentuk [2, B, hidden_dim]."""
        if device is None:
            device = next(self.parameters()).device
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_dim, device=device)
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_dim, device=device)
        return h0, c0

    def forward(self, input_ids: torch.Tensor, state: tuple = None):
        """Forward batch sequence input_ids [B, T].

        Args:
            input_ids: int64 tensor berbentuk [B, T]
            state: tuple opsional (h0, c0) masing-masing [num_layers, B, hidden_dim]

        Returns:
            logits: float32 tensor [B, T, vocab_size]
            (h_last, c_last): state terakhir [num_layers, B, hidden_dim]
        """
        B, T = input_ids.shape
        device = input_ids.device

        if state is None:
            h, c = self.init_hidden(B, device=device)
        else:
            h, c = state

        # Embed sequence token: [B, T, E]
        emb = self.embedding(input_ids)

        h1 = h[0]  # [B, hidden_dim]
        c1 = c[0]
        h2 = h[1]
        c2 = c[1]

        outputs = []
        for t in range(T):
            x_t = emb[:, t, :]  # [B, embedding_dim]
            h1, c1 = self.cell_layer1(x_t, h1, c1)
            h2, c2 = self.cell_layer2(h1, h2, c2)
            outputs.append(h2)

        # Gabungkan hidden state layer 2 untuk seluruh time step: [B, T, hidden_dim]
        lstm_out = torch.stack(outputs, dim=1)

        # Linear projection ke logits: [B, T, vocab_size]
        logits = self.head(lstm_out)

        h_last = torch.stack([h1, h2], dim=0)
        c_last = torch.stack([c1, c2], dim=0)

        return logits, (h_last, c_last)

    def step(self, token_id: torch.Tensor, state: tuple):
        """Inference satu langkah untuk autoregressive sampling.

        Args:
            token_id: int64 tensor [B, 1] atau [B]
            state: tuple (h, c) masing-masing [2, B, hidden_dim]

        Returns:
            logits_step: [B, vocab_size]
            new_state: tuple (new_h, new_c) masing-masing [2, B, hidden_dim]
        """
        if token_id.dim() == 1:
            token_id = token_id.unsqueeze(1)  # jadikan [B, 1]

        B = token_id.shape[0]
        h, c = state

        x = self.embedding(token_id)[:, 0, :]  # [B, embedding_dim]
        h1, c1 = self.cell_layer1(x, h[0], c[0])
        h2, c2 = self.cell_layer2(h1, h[1], c[1])

        logits = self.head(h2)  # [B, vocab_size]
        new_h = torch.stack([h1, h2], dim=0)
        new_c = torch.stack([c1, c2], dim=0)

        return logits, (new_h, new_c)

    def count_parameters(self) -> int:
        """Hitung total trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def create_model(
    vocab_size: int = VOCAB_SIZE,
    embedding_dim: int = EMBEDDING_DIM,
    hidden_dim: int = HIDDEN_DIM,
    num_layers: int = NUM_LAYERS,
) -> NiravaLSTMLanguageModel:
    """Helper factory pembuat model dengan konfigurasi default nirava-midi-lstm-v1."""
    return NiravaLSTMLanguageModel(
        vocab_size=vocab_size,
        embedding_dim=embedding_dim,
        hidden_dim=hidden_dim,
        num_layers=num_layers,
    )
