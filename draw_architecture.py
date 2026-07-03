import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Windows 한글 폰트 설정
for fname in ['malgun.ttf', 'malgunbd.ttf', 'NanumGothic.ttf']:
    import os, glob
    paths = glob.glob(f'C:/Windows/Fonts/{fname}')
    if paths:
        fm.fontManager.addfont(paths[0])
        matplotlib.rcParams['font.family'] = fm.FontProperties(fname=paths[0]).get_name()
        break
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(22, 16))
ax.set_xlim(0, 22)
ax.set_ylim(0, 16)
ax.axis('off')
fig.patch.set_facecolor('#F8F9FA')

# ── 색상 팔레트 ──────────────────────────────────────────────
C_INPUT    = '#4A90D9'
C_BACKBONE = '#2ECC71'
C_GAP      = '#F39C12'
C_FEATURE  = '#9B59B6'
C_HEAD     = '#E74C3C'
C_HEAD_CAT = '#E67E22'
C_OUTPUT   = '#1ABC9C'
C_ARROW    = '#555555'

def box(ax, x, y, w, h, color, text, fontsize=10, text_color='white', radius=0.3, alpha=1.0):
    patch = FancyBboxPatch((x - w/2, y - h/2), w, h,
                           boxstyle=f"round,pad=0.05,rounding_size={radius}",
                           facecolor=color, edgecolor='white',
                           linewidth=1.5, alpha=alpha, zorder=3)
    ax.add_patch(patch)
    lines = text.split('\n')
    for i, line in enumerate(lines):
        offset = (len(lines) - 1) / 2 * 0.18 - i * 0.18
        fs = fontsize if i == 0 else fontsize - 1
        fw = 'bold' if i == 0 else 'normal'
        ax.text(x, y + offset, line, ha='center', va='center',
                fontsize=fs, color=text_color, fontweight=fw, zorder=4)

def arrow(ax, x1, y1, x2, y2, color=C_ARROW, lw=1.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=lw, connectionstyle='arc3,rad=0'))

def label(ax, x, y, text, fontsize=8, color='#555555'):
    ax.text(x, y, text, ha='center', va='center',
            fontsize=fontsize, color=color, style='italic', zorder=4)

# ══════════════════════════════════════════════════════════════
# 제목
ax.text(11, 15.4, 'EfficientNet-B3 기반 멀티태스크 안구 질환 분류 모델',
        ha='center', va='center', fontsize=16, fontweight='bold', color='#2C3E50', zorder=4)
ax.text(11, 15.0, 'MultiTaskEyeDiseaseModel — 강아지(10종) / 고양이(5종) 독립 모델',
        ha='center', va='center', fontsize=11, color='#555555', zorder=4)

# ══════════════════════════════════════════════════════════════
# 1. 입력
box(ax, 11, 13.8, 3.2, 0.9, C_INPUT,
    '입력 이미지\n300 × 300 × 3 (RGB)', fontsize=10)
label(ax, 14.2, 13.8, 'Tensor: [B, 3, 300, 300]', 8)

arrow(ax, 11, 13.35, 11, 12.75)

# ══════════════════════════════════════════════════════════════
# 2. EfficientNet-B3 백본 (큰 박스)
backbone_bg = FancyBboxPatch((5.5, 9.6), 11, 2.9,
    boxstyle="round,pad=0.1,rounding_size=0.4",
    facecolor='#D5F5E3', edgecolor=C_BACKBONE, linewidth=2.5, alpha=0.6, zorder=1)
ax.add_patch(backbone_bg)
ax.text(11, 12.35, 'EfficientNet-B3 Backbone  (ImageNet Pretrained)',
        ha='center', va='center', fontsize=11, fontweight='bold', color='#1A5E31', zorder=4)

stages = [
    ('Stem\n3→40ch', 6.3),
    ('MBConv×2\n40→24ch', 7.5),
    ('MBConv×3\n24→48ch', 8.7),
    ('MBConv×3\n48→96ch', 9.9),
    ('MBConv×5\n96→136ch', 11.1),
    ('MBConv×5\n136→232ch', 12.3),
    ('MBConv×6\n232→384ch', 13.5),
    ('Head Conv\n384→1536ch', 14.7),
]
for txt, cx in stages:
    box(ax, cx, 11.2, 1.05, 1.3, C_BACKBONE, txt, fontsize=7.5, radius=0.2)
    if cx < 14.7:
        arrow(ax, cx + 0.53, 11.2, cx + 0.97, 11.2)

# stride / resolution 힌트
ax.text(6.3,  10.1, '150×150', ha='center', fontsize=7, color='#777')
ax.text(9.9,  10.1, '19×19',   ha='center', fontsize=7, color='#777')
ax.text(14.7, 10.1, '10×10',   ha='center', fontsize=7, color='#777')

arrow(ax, 11, 9.6, 11, 9.05)

# ══════════════════════════════════════════════════════════════
# 3. Global Average Pooling
box(ax, 11, 8.65, 3.2, 0.75, C_GAP,
    'Global Average Pooling', fontsize=10)
label(ax, 14.4, 8.65, '[B, 1536, 10, 10] → [B, 1536]', 8)

arrow(ax, 11, 8.28, 11, 7.7)

# ══════════════════════════════════════════════════════════════
# 4. 공유 특징 벡터
box(ax, 11, 7.35, 3.2, 0.65, C_FEATURE,
    '공유 특징 벡터  (1536-dim)', fontsize=10)
label(ax, 14.5, 7.35, 'Shared Feature [B, 1536]', 8)

# ── 분기 화살표 (강아지 / 고양이) ─────────────────────────
# 좌측 → 강아지
ax.annotate('', xy=(5.0, 6.4), xytext=(9.4, 7.05),
    arrowprops=dict(arrowstyle='->', color=C_HEAD, lw=1.8,
                    connectionstyle='arc3,rad=-0.15'))
# 우측 → 고양이
ax.annotate('', xy=(17.0, 6.4), xytext=(12.6, 7.05),
    arrowprops=dict(arrowstyle='->', color=C_HEAD_CAT, lw=1.8,
                    connectionstyle='arc3,rad=0.15'))

ax.text(5.5,  6.65, '강아지 모델', ha='center', fontsize=9,
        color=C_HEAD, fontweight='bold')
ax.text(16.5, 6.65, '고양이 모델', ha='center', fontsize=9,
        color=C_HEAD_CAT, fontweight='bold')

# ══════════════════════════════════════════════════════════════
# 5. 강아지 헤드 (10개)
dog_diseases = [
    ('결막염',        2),
    ('궤양성각막질환', 3),
    ('백내장',        4),
    ('비궤양성각막질환',3),
    ('색소침착성각막염',2),
    ('안검내반증',     2),
    ('안검염',        2),
    ('안검종양',      2),
    ('유루증',        2),
    ('핵경화',        2),
]

n_dog = len(dog_diseases)
dog_xs = [i * 0.98 + 0.55 for i in range(n_dog)]  # x positions

# 헤드 공통 구조 박스 (배경)
head_bg_dog = FancyBboxPatch((0.05, 0.5), 9.85, 5.65,
    boxstyle="round,pad=0.1,rounding_size=0.4",
    facecolor='#FADBD8', edgecolor=C_HEAD, linewidth=1.5, alpha=0.4, zorder=1)
ax.add_patch(head_bg_dog)
ax.text(5.0, 5.9, '멀티태스크 분류 헤드 — 강아지 (10종)',
        ha='center', fontsize=9.5, fontweight='bold', color='#922B21', zorder=4)

# 각 헤드
for i, (name, nc) in enumerate(dog_diseases):
    cx = dog_xs[i]
    # Dropout → FC(512)
    box(ax, cx, 5.3, 0.85, 0.52, '#C0392B',
        'Drop\n→FC512', fontsize=6.5, radius=0.15)
    arrow(ax, cx, 5.03, cx, 4.62)
    # ReLU → Dropout
    box(ax, cx, 4.3, 0.85, 0.52, '#E74C3C',
        'ReLU\nDrop', fontsize=6.5, radius=0.15)
    arrow(ax, cx, 4.03, cx, 3.62)
    # FC(n_classes)
    box(ax, cx, 3.3, 0.85, 0.52, '#C0392B',
        f'FC({nc})', fontsize=7, radius=0.15)
    arrow(ax, cx, 3.03, cx, 2.52)
    # 출력
    box(ax, cx, 2.2, 0.85, 0.52, C_OUTPUT,
        name, fontsize=6, radius=0.15)
    label(ax, cx, 1.75, f'{nc}cls', 6.5, '#1A5276')

# ══════════════════════════════════════════════════════════════
# 6. 고양이 헤드 (5개)
cat_diseases = [
    ('각막궤양',    2),
    ('각막부골편',  2),
    ('결막염',      2),
    ('비궤양성각막염',2),
    ('안검염',      2),
]
n_cat = len(cat_diseases)
cat_xs = [12.1 + i * 1.75 for i in range(n_cat)]

head_bg_cat = FancyBboxPatch((11.2, 0.5), 9.75, 5.65,
    boxstyle="round,pad=0.1,rounding_size=0.4",
    facecolor='#FDEBD0', edgecolor=C_HEAD_CAT, linewidth=1.5, alpha=0.4, zorder=1)
ax.add_patch(head_bg_cat)
ax.text(16.1, 5.9, '멀티태스크 분류 헤드 — 고양이 (5종)',
        ha='center', fontsize=9.5, fontweight='bold', color='#784212', zorder=4)

for i, (name, nc) in enumerate(cat_diseases):
    cx = cat_xs[i]
    box(ax, cx, 5.3, 1.45, 0.52, '#D35400',
        'Dropout(0.4) → FC(512)', fontsize=6.5, radius=0.15)
    arrow(ax, cx, 5.03, cx, 4.62)
    box(ax, cx, 4.3, 1.45, 0.52, '#E67E22',
        'ReLU → Dropout(0.5)', fontsize=6.5, radius=0.15)
    arrow(ax, cx, 4.03, cx, 3.62)
    box(ax, cx, 3.3, 1.45, 0.52, '#D35400',
        f'FC({nc} classes)', fontsize=7, radius=0.15)
    arrow(ax, cx, 3.03, cx, 2.52)
    box(ax, cx, 2.2, 1.45, 0.52, C_OUTPUT,
        name, fontsize=7.5, radius=0.15)
    label(ax, cx, 1.75, f'{nc} classes', 7, '#1A5276')

# ══════════════════════════════════════════════════════════════
# 7. 범례
legend_items = [
    mpatches.Patch(color=C_INPUT,    label='입력 레이어'),
    mpatches.Patch(color=C_BACKBONE, label='EfficientNet-B3 백본'),
    mpatches.Patch(color=C_GAP,      label='Global Average Pooling'),
    mpatches.Patch(color=C_FEATURE,  label='공유 특징 벡터 (1536-dim)'),
    mpatches.Patch(color=C_HEAD,     label='강아지 분류 헤드 (10종)'),
    mpatches.Patch(color=C_HEAD_CAT, label='고양이 분류 헤드 (5종)'),
    mpatches.Patch(color=C_OUTPUT,   label='질환별 확률 출력'),
]
ax.legend(handles=legend_items, loc='lower center',
          bbox_to_anchor=(0.5, -0.01), ncol=7,
          fontsize=8.5, framealpha=0.9, edgecolor='#CCCCCC')

# ══════════════════════════════════════════════════════════════
# 저장
out = r'C:\Capstone_GANADI\EfficientNetB3_MultiTask_Architecture.png'
plt.tight_layout(pad=0.5)
plt.savefig(out, dpi=180, bbox_inches='tight',
            facecolor=fig.get_facecolor())
print(f'저장 완료: {out}')
