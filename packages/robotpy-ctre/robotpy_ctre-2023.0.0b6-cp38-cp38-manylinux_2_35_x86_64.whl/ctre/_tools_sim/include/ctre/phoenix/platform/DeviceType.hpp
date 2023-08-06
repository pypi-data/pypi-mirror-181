/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

namespace ctre {
namespace phoenix {
namespace platform {

    /** List of all supported device types */
    #define kDeviceTypeListInitializer	\
        TalonSRXType,	\
        VictorSPXType,	\
        PigeonIMUType,	\
        RibbonPigeonIMUType,	\
        TalonFXType,	\
        CANCoderType,	\
        PRO_TalonFXType,	\
        PRO_CANcoderType,	\
        PRO_Pigeon2Type

    /** Enumeration of all supported device types. */
    enum DeviceType {kDeviceTypeListInitializer};

}
}
}
