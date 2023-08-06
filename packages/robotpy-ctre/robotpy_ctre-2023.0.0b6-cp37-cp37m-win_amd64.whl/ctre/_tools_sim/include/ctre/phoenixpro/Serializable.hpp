/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include <string>

namespace ctre {
namespace phoenixpro {

    class ISerializable
    {
    public:
        virtual std::string Serialize() const = 0;
    };

}
}
