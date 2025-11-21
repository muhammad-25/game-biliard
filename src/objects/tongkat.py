import math
import pygame

class Tongkat:
    """Trajectory-only aiming helper (no cue image).
    Draws dashed predicted path with short shadow balls while aiming.
    Has configurable shot force multiplier to increase hit power.
    """

    def __init__(self, asset_dir=None):
        # aiming state
        self.aiming = False
        self.target_ball = None
        self.aim_pos = (0, 0)

        # pull/shot tuning
        self.max_pull_px = 220.0
        self.pull_to_speed = 4.0      # base conversion pull(px) -> speed
        self.min_pull_required = 6.0
        self.pull_visual_factor = 0.9
        self.max_ball_speed_to_aim = 8.0

        # --- NEW: shot force multiplier (tweak this to increase/decrease shot strength) ---
        # Example: 1.0 = original strength, 2.0 = twice stronger
        self.shot_force_multiplier = 1.8

        # trajectory drawing params
        self.show_trajectory = True
        self.dash_len = 12
        self.space_len = 8
        self.traj_color = (230, 230, 200)
        self.traj_width = 3

        # shadow balls (shorter / fewer)
        self.show_shadow_balls = True
        self.shadow_ball_radius = 6
        self.shadow_ball_alpha = 160  # base alpha 0..255
        self.shadow_spacing = 64  # px between shadow markers (bigger = fewer markers)
        self.max_shadow_markers = 6  # hard limit on drawn shadow markers

        # tracing limits (shorter path)
        self.max_reflections = 2
        self.max_total_len = 700.0  # SHORTER overall path

    # -------------------------
    # Input handling / aiming
    # -------------------------
    def start_aim(self, target_ball, mouse_pos):
        if target_ball is None:
            return
        speed = math.hypot(getattr(target_ball, "vx", 0.0),
                           getattr(target_ball, "vy", 0.0))
        if speed > self.max_ball_speed_to_aim:
            return
        self.aiming = True
        self.target_ball = target_ball
        self.aim_pos = mouse_pos

    def update_aim(self, mouse_pos):
        if self.aiming:
            self.aim_pos = mouse_pos

    def release(self, mouse_pos):
        if not self.aiming or not self.target_ball:
            self._clear_state()
            return

        bx, by = self.target_ball.x, self.target_ball.y
        mx, my = mouse_pos
        dx = mx - bx
        dy = my - by
        dist = math.hypot(dx, dy)
        if dist < self.min_pull_required:
            self._clear_state()
            return

        dir_x = dx / dist
        dir_y = dy / dist

        pull = min(dist, self.max_pull_px)

        # --- APPLY MULTIPLIER HERE ---
        speed = pull * self.pull_to_speed * self.shot_force_multiplier

        # shot direction is opposite the pull vector
        self.target_ball.set_velocity(-dir_x * speed, -dir_y * speed)

        self._clear_state()

    # -------------------------
    # Drawing
    # -------------------------
    def draw(self, surface):
        if not self.aiming or not self.target_ball:
            return

        bx = float(self.target_ball.x)
        by = float(self.target_ball.y)
        mx, my = self.aim_pos

        dx = mx - bx
        dy = my - by
        dist = math.hypot(dx, dy)
        if dist == 0:
            return

        # shot direction (opposite pull): from ball going toward shot_dir
        dir_x = -dx / dist
        dir_y = -dy / dist

        # compute predicted polyline with reflections
        segs = self._compute_reflected_path(bx, by, dir_x, dir_y, self.target_ball.radius,
                                            self.max_reflections, self.max_total_len, surface.get_size())

        # draw dashed polyline
        if self.show_trajectory and segs:
            for a, b in segs:
                self._draw_dashed_line(surface, self.traj_color, a, b, self.dash_len, self.space_len, self.traj_width)

        # draw shadow balls along path (limited / fading)
        if self.show_shadow_balls and segs:
            self._draw_shadow_markers(surface, segs, spacing=self.shadow_spacing, max_markers=self.max_shadow_markers)

        # small markers at ball center and mouse handle
        pygame.draw.circle(surface, (255, 80, 80), (int(bx), int(by)), 3)  # ball center
        pygame.draw.circle(surface, (80, 200, 255), (int(mx), int(my)), 6)  # handle

        # --- draw a small power indicator near the handle so you can see current effective power ---
        try:
            pull = min(dist, self.max_pull_px)
            effective_speed = int(pull * self.pull_to_speed * self.shot_force_multiplier)
            font = pygame.font.SysFont(None, 18)
            text = font.render(f"Power: {effective_speed}", True, (240,240,240))
            surface.blit(text, (int(mx) + 10, int(my) - 18))
        except Exception:
            pass

    # -------------------------
    # Path computation helpers
    # -------------------------
    def _compute_reflected_path(self, x, y, dx, dy, radius, max_reflections, max_total_len, screen_size):
        """Simulate a ray starting at (x,y) in direction (dx,dy) with reflections
        on the axis-aligned rectangle [0..w]x[0..h]. Returns list of segments [(x1,y1),(x2,y2), ...].
        """
        w, h = screen_size
        segments = []
        remaining = max_total_len
        cur_x = x
        cur_y = y
        dir_x = dx
        dir_y = dy

        for _ in range(max_reflections):
            if remaining <= 0:
                break

            # find t to vertical walls considering radius (so ball edge hits)
            t_x = float("inf")
            if abs(dir_x) > 1e-9:
                if dir_x > 0:
                    wall_x = w - radius
                else:
                    wall_x = radius
                t = (wall_x - cur_x) / dir_x
                if t > 1e-6:
                    t_x = t
            # find t to horizontal walls
            t_y = float("inf")
            if abs(dir_y) > 1e-9:
                if dir_y > 0:
                    wall_y = h - radius
                else:
                    wall_y = radius
                t = (wall_y - cur_y) / dir_y
                if t > 1e-6:
                    t_y = t

            if t_x == float("inf") and t_y == float("inf"):
                # extend by remaining length
                ex = cur_x + dir_x * remaining
                ey = cur_y + dir_y * remaining
                segments.append(((cur_x, cur_y), (ex, ey)))
                remaining = 0
                break

            # choose nearest hit
            if t_x < t_y:
                t_hit = t_x
                hit_axis = "vertical"
            else:
                t_hit = t_y
                hit_axis = "horizontal"

            seg_len = min(t_hit, remaining)
            nx = cur_x + dir_x * seg_len
            ny = cur_y + dir_y * seg_len
            segments.append(((cur_x, cur_y), (nx, ny)))
            remaining -= seg_len

            if seg_len < t_hit - 1e-6:
                # stopped because of remaining limit
                break

            # move to hit point and reflect
            cur_x = nx
            cur_y = ny
            if hit_axis == "vertical":
                dir_x = -dir_x
            else:
                dir_y = -dir_y

        # extend a little if remaining > 0
        if remaining > 0:
            ex = cur_x + dir_x * remaining
            ey = cur_y + dir_y * remaining
            segments.append(((cur_x, cur_y), (ex, ey)))

        return segments

    # -------------------------
    # Drawing utilities
    # -------------------------
    def _draw_dashed_line(self, surface, color, start, end, dash_len=12, space_len=8, width=3):
        """Draw dashed line from start->end."""
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        seg_len = math.hypot(dx, dy)
        if seg_len < 1e-6:
            return
        ux = dx / seg_len
        uy = dy / seg_len

        drawn = 0.0
        pos_x = x1
        pos_y = y1
        draw_on = True
        while drawn < seg_len:
            chunk = dash_len if draw_on else space_len
            take = min(chunk, seg_len - drawn)
            nxt_x = pos_x + ux * take
            nxt_y = pos_y + uy * take
            if draw_on:
                pygame.draw.line(surface, color, (int(pos_x), int(pos_y)), (int(nxt_x), int(nxt_y)), width)
            pos_x, pos_y = nxt_x, nxt_y
            drawn += take
            draw_on = not draw_on

    def _draw_shadow_markers(self, surface, segments, spacing=48, max_markers=6):
        """Draw semi-transparent small circles along the polyline segments at interval = spacing.
        Limits number of markers to max_markers; fades alpha for further markers.
        """
        # collect points along polyline spaced by 'spacing'
        points = []
        rem = 0.0
        total_len = 0.0
        for a, b in segments:
            ax, ay = a
            bx, by = b
            seg_dx = bx - ax
            seg_dy = by - ay
            seg_len = math.hypot(seg_dx, seg_dy)
            if seg_len == 0:
                continue
            pos_t = 0.0
            while pos_t < seg_len and len(points) < max_markers:
                need = spacing - rem if rem > 1e-9 else spacing
                if pos_t + need <= seg_len + 1e-6:
                    t = (pos_t + need) / seg_len
                    px = ax + seg_dx * t
                    py = ay + seg_dy * t
                    points.append((px, py))
                    pos_t += need
                    rem = 0.0
                else:
                    rem += seg_len - pos_t
                    pos_t = seg_len
            total_len += seg_len
            if len(points) >= max_markers:
                break

        if not points:
            return

        # draw points with decreasing alpha
        tmp = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        for i, (px, py) in enumerate(points):
            # fade alpha: earliest markers more visible, later markers fainter
            frac = 1.0 - (i / max(1, len(points) - 1)) if len(points) > 1 else 1.0
            alpha = int(self.shadow_ball_alpha * (0.5 + 0.5 * frac))  # range ~50%..100%
            col = (200, 200, 200, max(30, min(255, alpha)))
            pygame.draw.circle(tmp, col, (int(px), int(py)), self.shadow_ball_radius)
        surface.blit(tmp, (0, 0))

    # -------------------------
    # helper
    # -------------------------
    def _clear_state(self):
        self.aiming = False
        self.target_ball = None
        self.aim_pos = (0, 0)
