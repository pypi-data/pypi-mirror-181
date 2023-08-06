#pragma once

#include "../machine.hpp"
#include "../system.hpp"
#include "../vec2.hpp"

#include <pybind11/detail/common.h>
#include <pybind11/pybind11.h>

#include <string>
#include <tuple>

namespace py = pybind11;

inline auto add_screen_class(py::module_ const& mod)
{
    auto screen = py::class_<Screen, std::shared_ptr<Screen>>(mod, "Screen");
    screen.def("set_as_target", &Screen::set_target);
    screen.def_property_readonly("frame_counter", [](Screen const&) {
        return Machine::get_instance().frame_counter;
    });
    screen.def_property_readonly("context", [](Screen const&) {
        return Machine::get_instance().context;
    });
    screen.def_property_readonly(
        "size", [](Screen const& screen) { return Vec2i{screen.get_size()}; });
    screen.def_property_readonly(
        "width", [](Screen const& s) { return s.get_size().first; });
    screen.def_property_readonly(
        "height", [](Screen const& s) { return s.get_size().second; });
    screen.def(
        "swap",
        [](std::shared_ptr<Screen> const& screen) {
            auto& m = Machine::get_instance();
            m.frame_counter++;
            m.context->flush();
            screen->swap();
        },
        "Synchronize with the frame rate of the display and swap buffers. This "
        "is normally the last thing you do in your render loop.");

    return screen;
}
