#pragma once

#include "colors.hpp"
#include "gl/buffer.hpp"
#include "gl/color.hpp"
#include "gl/functions.hpp"
#include "gl/program.hpp"
#include "gl/program_cache.hpp"
#include "gl/texture.hpp"

#include "vec2.hpp"

namespace pix {

class Context
{
    GLuint target = 0;
    Vec2f offset{0, 0};

public:
    Vec2i clip_start{0,0};
    Vec2i clip_size{0,0};

    Vec2f target_size;
    float vpscale = 1.0F;

    float line_width = 1;
    float point_size = 2;
    gl_wrap::Color fg;

    std::vector<float> points;

private:
    Vec2f last_point{0,0};

    gl_wrap::Program& colored;
    gl_wrap::Program& textured;
    gl_wrap::Program& filled;

    template <typename CO>
    void draw_filled(CO const& container, gl_wrap::Primitive primitive);

    template <typename CO>
    void draw_textured(CO const& container, gl_wrap::Primitive primitive);

    std::vector<float> generate_circle(Vec2f center, float radius,
                                       bool include_center = true) const;
    std::array<float, 4> generate_line(Vec2f from, Vec2f to) const;
    std::vector<float> generate_lines(float const* screen_cords, int count) const;
    std::array<float, 8> generate_quad(Vec2f top_left, Vec2f size) const;
    std::array<float, 8> rotated_quad(Vec2f center, Vec2f sz, float rot) const;
    std::array<float, 16> generate_quad_with_uvs(Vec2f pos, Vec2f size) const;

    std::array<float, 16> rotated_quad_with_uvs(Vec2f center, Vec2f sz,
                                                float rot) const;

    void draw_points();

public:
    constexpr Vec2<float> to_screen(Vec2f const& v) const
    {
        auto res = (v + offset) * Vec2f{2, -2} / target_size + Vec2f{-1, 1};
        return {static_cast<float>(res.x), static_cast<float>(res.y)};
    }

    constexpr Vec2<float> to_screen(float x, float y) const
    {
        return to_screen(Vec2f{x, y});
    }

    Context(float w, float h, GLuint fb = 0);
    Context(Vec2f const& offset, Vec2f const& size, GLuint fb = 0);

    Vec2f const& screen_size() { return target_size; }

    void set_target() const;

    void set_color(gl_wrap::Color const& col);

    void circle(Vec2f const& v, float r);
    void filled_circle(Vec2f const& v, float r);
    void line(Vec2f from, Vec2f to);
    void line(Vec2f to);
    void filled_rect(Vec2f top_left, Vec2f size);
    void rect(Vec2f top_left, Vec2f size);
    void blit(gl_wrap::TexRef const& tex, Vec2f pos, Vec2f size);
    void draw(gl_wrap::TexRef const& tex, Vec2f center, Vec2f size, float rot);

    void plot(Vec2f point, gl_wrap::Color col);
    void flush();


    void clear(gl_wrap::Color const& col) const;
    void draw_polygon(const Vec2f* points, size_t count);
};
} // namespace pix
