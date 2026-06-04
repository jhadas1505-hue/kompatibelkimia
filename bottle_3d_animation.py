"""
Module untuk membuat animasi 3D botol penyimpan bahan kimia
dengan efek interaktif dan reaksi kompatibilitas
"""

import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

def create_bottle_3d(x_offset=0, y_offset=0, z_offset=0, color="#00d4ff", label="Bottle 1"):
    """
    Membuat model 3D botol penyimpan bahan kimia
    
    Parameters:
    - x_offset: posisi X
    - y_offset: posisi Y  
    - z_offset: posisi Z
    - color: warna botol
    - label: label botol
    
    Returns: dict dengan data botol 3D
    """
    
    # Buat botol dengan kombinasi shape geometri
    # Bagian bawah (tabung)
    theta = np.linspace(0, 2*np.pi, 50)
    z_bottom = np.linspace(-2, 0, 30)
    theta_grid, z_grid = np.meshgrid(theta, z_bottom)
    
    x_bottom = 0.8 * np.cos(theta_grid) + x_offset
    y_bottom = 0.8 * np.sin(theta_grid) + y_offset
    z_bottom_grid = z_grid + z_offset
    
    # Bagian leher (lebih sempit)
    theta2 = np.linspace(0, 2*np.pi, 50)
    z_neck = np.linspace(0, 1.2, 20)
    theta_grid2, z_grid2 = np.meshgrid(theta2, z_neck)
    
    x_neck = (0.8 - 0.3 * (z_grid2 / 1.2)) * np.cos(theta_grid2) + x_offset
    y_neck = (0.8 - 0.3 * (z_grid2 / 1.2)) * np.sin(theta_grid2) + y_offset
    z_neck_grid = z_grid2 + z_offset
    
    # Cap/tutup botol
    theta3 = np.linspace(0, 2*np.pi, 50)
    z_cap = np.linspace(1.2, 1.5, 10)
    theta_grid3, z_grid3 = np.meshgrid(theta3, z_cap)
    
    x_cap = 0.5 * np.cos(theta_grid3) + x_offset
    y_cap = 0.5 * np.sin(theta_grid3) + y_offset
    z_cap_grid = z_grid3 + z_offset
    
    # Cairan di dalam botol
    z_liquid = np.linspace(-2, -0.5, 15)
    theta_liquid = np.linspace(0, 2*np.pi, 50)
    theta_grid_liquid, z_grid_liquid = np.meshgrid(theta_liquid, z_liquid)
    
    x_liquid = 0.75 * np.cos(theta_grid_liquid) + x_offset
    y_liquid = 0.75 * np.sin(theta_grid_liquid) + y_offset
    z_liquid_grid = z_grid_liquid + z_offset
    
    return {
        'x_bottom': x_bottom,
        'y_bottom': y_bottom,
        'z_bottom': z_bottom_grid,
        'x_neck': x_neck,
        'y_neck': y_neck,
        'z_neck': z_neck_grid,
        'x_cap': x_cap,
        'y_cap': y_cap,
        'z_cap': z_cap_grid,
        'x_liquid': x_liquid,
        'y_liquid': y_liquid,
        'z_liquid': z_liquid_grid,
        'color': color,
        'label': label
    }


def add_bottle_to_figure(fig, bottle_data, surface_color, liquid_color, opacity=0.8):
    """Menambahkan botol ke figure Plotly"""
    
    # Tambah permukaan botol (bawah)
    fig.add_trace(go.Surface(
        x=bottle_data['x_bottom'],
        y=bottle_data['y_bottom'],
        z=bottle_data['z_bottom'],
        colorscale=[[0, surface_color], [1, surface_color]],
        showscale=False,
        opacity=opacity,
        name=f"{bottle_data['label']} (Body)",
        hoverinfo='text',
        text=f"<b>{bottle_data['label']}</b><br>Body"
    ))
    
    # Tambah leher botol
    fig.add_trace(go.Surface(
        x=bottle_data['x_neck'],
        y=bottle_data['y_neck'],
        z=bottle_data['z_neck'],
        colorscale=[[0, surface_color], [1, surface_color]],
        showscale=False,
        opacity=opacity,
        name=f"{bottle_data['label']} (Neck)",
        hoverinfo='text',
        text=f"<b>{bottle_data['label']}</b><br>Neck"
    ))
    
    # Tambah cap/tutup
    fig.add_trace(go.Surface(
        x=bottle_data['x_cap'],
        y=bottle_data['y_cap'],
        z=bottle_data['z_cap'],
        colorscale=[[0, '#ff9500'], [1, '#ff6b00']],
        showscale=False,
        opacity=0.9,
        name=f"{bottle_data['label']} (Cap)",
        hoverinfo='text',
        text=f"<b>{bottle_data['label']}</b><br>Cap"
    ))
    
    # Tambah cairan di dalam
    fig.add_trace(go.Surface(
        x=bottle_data['x_liquid'],
        y=bottle_data['y_liquid'],
        z=bottle_data['z_liquid'],
        colorscale=[[0, liquid_color], [1, liquid_color]],
        showscale=False,
        opacity=0.7,
        name=f"{bottle_data['label']} (Liquid)",
        hoverinfo='text',
        text=f"<b>{bottle_data['label']}</b><br>Liquid Content"
    ))


def create_compatibility_animation_3d(chem1_name, chem1_category, chem2_name, chem2_category, 
                                      status, bottle1_color="#00d4ff", bottle2_color="#ff006e"):
    """
    Membuat animasi 3D 2 botol bahan kimia yang saling didekatkan
    
    Parameters:
    - chem1_name: nama bahan kimia 1
    - chem1_category: kategori bahan kimia 1
    - chem2_name: nama bahan kimia 2
    - chem2_category: kategori bahan kimia 2
    - status: status kompatibilitas ("AMAN", "BERBAHAYA", "PERHATIAN")
    - bottle1_color: warna botol 1
    - bottle2_color: warna botol 2
    
    Returns: Plotly figure dengan animasi 3D
    """
    
    # Tentukan warna liquid berdasarkan kategori
    liquid_colors = {
        'Flammable': '#ff4444',
        'Corrosive': '#ffaa00',
        'Oxidizer': '#00aa00',
        'Toxic': '#9900ff',
        'Mixed': '#00ccff'
    }
    
    liquid_color1 = liquid_colors.get(chem1_category, '#4499ff')
    liquid_color2 = liquid_colors.get(chem2_category, '#ff4499')
    
    # Tentukan jumlah frame animasi
    n_frames = 100
    
    # Buat frame untuk animasi pergerakan botol
    frames = []
    
    for frame_num in range(n_frames):
        # Hitung posisi botol berdasarkan progress animasi
        t = frame_num / (n_frames - 1)  # 0 to 1
        
        # Botol 1 bergerak dari kiri ke tengah
        x1_pos = -3 + (3 * t)
        # Botol 2 bergerak dari kanan ke tengah
        x2_pos = 3 - (3 * t)
        
        # Efek rotasi
        rotation = t * 360
        
        # Buat botol untuk frame ini
        bottle1 = create_bottle_3d(x_offset=x1_pos, y_offset=0, z_offset=0, 
                                   color=bottle1_color, label=chem1_name)
        bottle2 = create_bottle_3d(x_offset=x2_pos, y_offset=0, z_offset=0, 
                                   color=bottle2_color, label=chem2_name)
        
        # Buat figure untuk frame ini
        fig_frame = go.Figure()
        
        # Tentukan opacity liquid berdasarkan status
        if "AMAN" in status:
            liquid_opacity1 = 0.5 + 0.3 * np.sin(t * np.pi)
            liquid_opacity2 = 0.5 + 0.3 * np.sin(t * np.pi)
        elif "BERBAHAYA" in status:
            liquid_opacity1 = 0.7 + 0.2 * np.sin(t * np.pi * 2)  # Bergerak cepat
            liquid_opacity2 = 0.7 + 0.2 * np.sin(t * np.pi * 2)
        else:  # PERHATIAN
            liquid_opacity1 = 0.6 + 0.2 * np.sin(t * np.pi)
            liquid_opacity2 = 0.6 + 0.2 * np.sin(t * np.pi)
        
        add_bottle_to_figure(fig_frame, bottle1, bottle1_color, liquid_color1, liquid_opacity1)
        add_bottle_to_figure(fig_frame, bottle2, bottle2_color, liquid_color2, liquid_opacity2)
        
        # Setup layout
        fig_frame.update_layout(
            scene=dict(
                xaxis=dict(range=[-4, 4], showgrid=True, zeroline=True),
                yaxis=dict(range=[-3, 3], showgrid=True, zeroline=True),
                zaxis=dict(range=[-3, 2], showgrid=True, zeroline=True),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5),
                    center=dict(x=0, y=0, z=0)
                ),
                aspectmode='cube'
            ),
            showlegend=False,
            hovermode='closest'
        )
        
        frames.append(go.Frame(data=fig_frame.data))
    
    # Buat figure utama dengan frame pertama
    fig = go.Figure(
        data=frames[0].data,
        frames=frames
    )
    
    # Setup layout dengan slider untuk kontrol animasi
    sliders = [dict(
        active=0,
        yanchor="top",
        y=0,
        xanchor="left",
        x=0.1,
        len=0.8,
        transition=dict(duration=50),
        pad=dict(b=10, t=50),
        currentvalue=dict(
            prefix="Progress: ",
            visible=True,
            xanchor="right",
            font=dict(size=16, color="#00d4ff")
        ),
        steps=[dict(
            args=[[f.name], dict(
                frame=dict(duration=50, redraw=True),
                mode="immediate",
                transition=dict(duration=50)
            )],
            method="animate",
            label=str(i)
        ) for i, f in enumerate(frames)]
    )]
    
    # Tentukan judul berdasarkan status
    title_color = "#00d97e" if "AMAN" in status else ("#ff006e" if "BERBAHAYA" in status else "#ffa500")
    
    fig.update_layout(
        title=dict(
            text=f"<b>3D Chemical Compatibility Animation</b><br><sub>{chem1_name} + {chem2_name} → {status}</sub>",
            font=dict(size=20, color=title_color),
            x=0.5,
            xanchor='center'
        ),
        scene=dict(
            xaxis=dict(
                range=[-4, 4],
                showgrid=True,
                zeroline=True,
                backgroundcolor="rgb(15, 15, 30)",
                gridcolor="rgb(50, 50, 100)",
                showbackground=True
            ),
            yaxis=dict(
                range=[-3, 3],
                showgrid=True,
                zeroline=True,
                backgroundcolor="rgb(15, 15, 30)",
                gridcolor="rgb(50, 50, 100)",
                showbackground=True
            ),
            zaxis=dict(
                range=[-3, 2],
                showgrid=True,
                zeroline=True,
                backgroundcolor="rgb(15, 15, 30)",
                gridcolor="rgb(50, 50, 100)",
                showbackground=True
            ),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5),
                center=dict(x=0, y=0, z=0)
            ),
            aspectmode='cube'
        ),
        paper_bgcolor='rgba(26, 26, 46, 0.9)',
        plot_bgcolor='rgba(26, 26, 46, 0.9)',
        font=dict(color='#eaeaea', family='Arial'),
        height=700,
        sliders=sliders,
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=[
                    dict(label="▶ Play",
                         method="animate",
                         args=[None, dict(
                             frame=dict(duration=50, redraw=True),
                             fromcurrent=True,
                             mode="immediate",
                             transition=dict(duration=50)
                         )]),
                    dict(label="⏸ Pause",
                         method="animate",
                         args=[[None], dict(
                             frame=dict(duration=0, redraw=False),
                             mode="immediate",
                             transition=dict(duration=0)
                         )])
                ],
                pad=dict(t=70),
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )
        ],
        showlegend=False,
        hovermode='closest'
    )
    
    return fig


def create_reaction_indicator(status):
    """
    Membuat indikator reaksi visual berdasarkan status kompatibilitas
    """
    
    if "AMAN" in status:
        color = "#00d97e"
        emoji = "✅"
        message = "AMAN - Kedua bahan dapat disimpan berdekatan"
    elif "BERBAHAYA" in status:
        color = "#ff006e"
        emoji = "❌"
        message = "BERBAHAYA - Kedua bahan TIDAK boleh berdekatan"
    else:
        color = "#ffa500"
        emoji = "⚠️"
        message = "PERHATIAN - Perlu perlakuan khusus"
    
    html = f"""
    <div style='
        background: linear-gradient(135deg, {color}40 0%, {color}20 100%);
        border: 3px solid {color};
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: {color};
        margin: 20px 0;
        animation: pulse 2s infinite;
    '>
        <div style='font-size: 40px; margin-bottom: 10px;'>{emoji}</div>
        <div>{message}</div>
    </div>
    <style>
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.8; }}
        }}
    </style>
    """
    
    return html
