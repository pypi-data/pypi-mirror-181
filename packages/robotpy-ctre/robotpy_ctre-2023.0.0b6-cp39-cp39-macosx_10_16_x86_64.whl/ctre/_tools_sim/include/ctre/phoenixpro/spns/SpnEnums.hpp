/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include "ctre/phoenixpro/Serializable.hpp"
#include <sstream>
#include <string>

namespace ctre {
namespace phoenixpro {
namespace spns {


/**
 * \brief  System state of the device
 */
class TalonFX_System_StateValue : public ISerializable
{
public:
    int value;

    static constexpr int Bootup_0 = 0;
    static constexpr int Bootup_1 = 1;
    static constexpr int Bootup_2 = 2;
    static constexpr int Bootup_3 = 3;
    static constexpr int Bootup_4 = 4;
    static constexpr int Bootup_5 = 5;
    static constexpr int BootBeep = 6;
    static constexpr int ControlDisabled = 7;
    static constexpr int ControlEnabled = 8;
    static constexpr int Fault = 9;
    static constexpr int Recover = 10;
    static constexpr int NotLicensed = 11;

    TalonFX_System_StateValue(int value) :
        value{value}
    {}

    TalonFX_System_StateValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case TalonFX_System_StateValue::Bootup_0: return "Bootup_0";
        case TalonFX_System_StateValue::Bootup_1: return "Bootup_1";
        case TalonFX_System_StateValue::Bootup_2: return "Bootup_2";
        case TalonFX_System_StateValue::Bootup_3: return "Bootup_3";
        case TalonFX_System_StateValue::Bootup_4: return "Bootup_4";
        case TalonFX_System_StateValue::Bootup_5: return "Bootup_5";
        case TalonFX_System_StateValue::BootBeep: return "BootBeep";
        case TalonFX_System_StateValue::ControlDisabled: return "ControlDisabled";
        case TalonFX_System_StateValue::ControlEnabled: return "ControlEnabled";
        case TalonFX_System_StateValue::Fault: return "Fault";
        case TalonFX_System_StateValue::Recover: return "Recover";
        case TalonFX_System_StateValue::NotLicensed: return "NotLicensed";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const TalonFX_System_StateValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const TalonFX_System_StateValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const TalonFX_System_StateValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  Magnet health as measured by CANcoder.
 *
 * \details  Magnet health as measured by CANcoder. Red indicates too close or
 *           too far, Orange is adequate but with reduced accuracy, green is
 *           ideal. Invalid means the accuracy cannot be determined.
 */
class CANcoder_MagHealthValue : public ISerializable
{
public:
    int value;

    static constexpr int Magnet_Red = 1;
    static constexpr int Magnet_Orange = 2;
    static constexpr int Magnet_Green = 3;
    static constexpr int Magnet_Invalid = 0;

    CANcoder_MagHealthValue(int value) :
        value{value}
    {}

    CANcoder_MagHealthValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case CANcoder_MagHealthValue::Magnet_Red: return "Magnet_Red";
        case CANcoder_MagHealthValue::Magnet_Orange: return "Magnet_Orange";
        case CANcoder_MagHealthValue::Magnet_Green: return "Magnet_Green";
        case CANcoder_MagHealthValue::Magnet_Invalid: return "Magnet_Invalid";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const CANcoder_MagHealthValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const CANcoder_MagHealthValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const CANcoder_MagHealthValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  Whether the device is pro licensed or not
 */
class Licensing_IsProLicensedValue : public ISerializable
{
public:
    int value;

    static constexpr int NotLicensed = 0;
    static constexpr int Licensed = 1;

    Licensing_IsProLicensedValue(int value) :
        value{value}
    {}

    Licensing_IsProLicensedValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case Licensing_IsProLicensedValue::NotLicensed: return "Not Licensed";
        case Licensing_IsProLicensedValue::Licensed: return "Licensed";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const Licensing_IsProLicensedValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const Licensing_IsProLicensedValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const Licensing_IsProLicensedValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  Direction of the sensor to determine positive facing the LED side of
 *         the CANcoder.
 */
class CANcoder_SensorDirectionValue : public ISerializable
{
public:
    int value;

    static constexpr int CounterClockwise_Positive = 0;
    static constexpr int Clockwise_Positive = 1;

    CANcoder_SensorDirectionValue(int value) :
        value{value}
    {}

    CANcoder_SensorDirectionValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case CANcoder_SensorDirectionValue::CounterClockwise_Positive: return "CounterClockwise_Positive";
        case CANcoder_SensorDirectionValue::Clockwise_Positive: return "Clockwise_Positive";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const CANcoder_SensorDirectionValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const CANcoder_SensorDirectionValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const CANcoder_SensorDirectionValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  True if device is locked by FRC.
 */
class FrcLockValue : public ISerializable
{
public:
    int value;

    static constexpr int Frc_Locked = 1;
    static constexpr int Frc_Unlocked = 0;

    FrcLockValue(int value) :
        value{value}
    {}

    FrcLockValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case FrcLockValue::Frc_Locked: return "Frc_Locked";
        case FrcLockValue::Frc_Unlocked: return "Frc_Unlocked";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const FrcLockValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const FrcLockValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const FrcLockValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  True if the robot is enabled.
 */
class RobotEnabledValue : public ISerializable
{
public:
    int value;

    static constexpr int Enabled = 1;
    static constexpr int Disabled = 0;

    RobotEnabledValue(int value) :
        value{value}
    {}

    RobotEnabledValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case RobotEnabledValue::Enabled: return "Enabled";
        case RobotEnabledValue::Disabled: return "Disabled";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const RobotEnabledValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const RobotEnabledValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const RobotEnabledValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  The Color of LED1 when it's "On".
 */
class LED1_OnColorValue : public ISerializable
{
public:
    int value;

    static constexpr int Off = 0;
    static constexpr int Red = 1;
    static constexpr int Green = 2;
    static constexpr int Orange = 3;
    static constexpr int Blue = 4;
    static constexpr int Pink = 5;
    static constexpr int Cyan = 6;
    static constexpr int White = 7;

    LED1_OnColorValue(int value) :
        value{value}
    {}

    LED1_OnColorValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case LED1_OnColorValue::Off: return "Off";
        case LED1_OnColorValue::Red: return "Red";
        case LED1_OnColorValue::Green: return "Green";
        case LED1_OnColorValue::Orange: return "Orange";
        case LED1_OnColorValue::Blue: return "Blue";
        case LED1_OnColorValue::Pink: return "Pink";
        case LED1_OnColorValue::Cyan: return "Cyan";
        case LED1_OnColorValue::White: return "White";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const LED1_OnColorValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const LED1_OnColorValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const LED1_OnColorValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  The Color of LED1 when it's "Off".
 */
class LED1_OffColorValue : public ISerializable
{
public:
    int value;

    static constexpr int Off = 0;
    static constexpr int Red = 1;
    static constexpr int Green = 2;
    static constexpr int Orange = 3;
    static constexpr int Blue = 4;
    static constexpr int Pink = 5;
    static constexpr int Cyan = 6;
    static constexpr int White = 7;

    LED1_OffColorValue(int value) :
        value{value}
    {}

    LED1_OffColorValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case LED1_OffColorValue::Off: return "Off";
        case LED1_OffColorValue::Red: return "Red";
        case LED1_OffColorValue::Green: return "Green";
        case LED1_OffColorValue::Orange: return "Orange";
        case LED1_OffColorValue::Blue: return "Blue";
        case LED1_OffColorValue::Pink: return "Pink";
        case LED1_OffColorValue::Cyan: return "Cyan";
        case LED1_OffColorValue::White: return "White";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const LED1_OffColorValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const LED1_OffColorValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const LED1_OffColorValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  The Color of LED2 when it's "On".
 */
class LED2_OnColorValue : public ISerializable
{
public:
    int value;

    static constexpr int Off = 0;
    static constexpr int Red = 1;
    static constexpr int Green = 2;
    static constexpr int Orange = 3;
    static constexpr int Blue = 4;
    static constexpr int Pink = 5;
    static constexpr int Cyan = 6;
    static constexpr int White = 7;

    LED2_OnColorValue(int value) :
        value{value}
    {}

    LED2_OnColorValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case LED2_OnColorValue::Off: return "Off";
        case LED2_OnColorValue::Red: return "Red";
        case LED2_OnColorValue::Green: return "Green";
        case LED2_OnColorValue::Orange: return "Orange";
        case LED2_OnColorValue::Blue: return "Blue";
        case LED2_OnColorValue::Pink: return "Pink";
        case LED2_OnColorValue::Cyan: return "Cyan";
        case LED2_OnColorValue::White: return "White";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const LED2_OnColorValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const LED2_OnColorValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const LED2_OnColorValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  The Color of LED2 when it's "Off".
 */
class LED2_OffColorValue : public ISerializable
{
public:
    int value;

    static constexpr int Off = 0;
    static constexpr int Red = 1;
    static constexpr int Green = 2;
    static constexpr int Orange = 3;
    static constexpr int Blue = 4;
    static constexpr int Pink = 5;
    static constexpr int Cyan = 6;
    static constexpr int White = 7;

    LED2_OffColorValue(int value) :
        value{value}
    {}

    LED2_OffColorValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case LED2_OffColorValue::Off: return "Off";
        case LED2_OffColorValue::Red: return "Red";
        case LED2_OffColorValue::Green: return "Green";
        case LED2_OffColorValue::Orange: return "Orange";
        case LED2_OffColorValue::Blue: return "Blue";
        case LED2_OffColorValue::Pink: return "Pink";
        case LED2_OffColorValue::Cyan: return "Cyan";
        case LED2_OffColorValue::White: return "White";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const LED2_OffColorValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const LED2_OffColorValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const LED2_OffColorValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  Invert state of the device
 */
class InvertedValue : public ISerializable
{
public:
    int value;

    static constexpr int CounterClockwise_Positive = 0;
    static constexpr int Clockwise_Positive = 1;

    InvertedValue(int value) :
        value{value}
    {}

    InvertedValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case InvertedValue::CounterClockwise_Positive: return "CounterClockwise_Positive";
        case InvertedValue::Clockwise_Positive: return "Clockwise_Positive";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const InvertedValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const InvertedValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const InvertedValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  The range of the absolute sensor, either [0-360) or [-180, 180).
 */
class CANcoder_AbsoluteSensorRangeValue : public ISerializable
{
public:
    int value;

    static constexpr int Unsigned_0To360 = 0;
    static constexpr int Signed_PlusMinus180 = 1;

    CANcoder_AbsoluteSensorRangeValue(int value) :
        value{value}
    {}

    CANcoder_AbsoluteSensorRangeValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case CANcoder_AbsoluteSensorRangeValue::Unsigned_0To360: return "Unsigned_0To360";
        case CANcoder_AbsoluteSensorRangeValue::Signed_PlusMinus180: return "Signed_PlusMinus180";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const CANcoder_AbsoluteSensorRangeValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const CANcoder_AbsoluteSensorRangeValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const CANcoder_AbsoluteSensorRangeValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  True if the device is enabled.
 */
class DeviceEnabledValue : public ISerializable
{
public:
    int value;

    static constexpr int Enabled = 1;
    static constexpr int Disabled = 0;

    DeviceEnabledValue(int value) :
        value{value}
    {}

    DeviceEnabledValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case DeviceEnabledValue::Enabled: return "Enabled";
        case DeviceEnabledValue::Disabled: return "Disabled";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const DeviceEnabledValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const DeviceEnabledValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const DeviceEnabledValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  Forward Limit Pin.
 */
class ForwardLimitValue : public ISerializable
{
public:
    int value;

    static constexpr int ClosedToGround = 0;
    static constexpr int Open = 1;

    ForwardLimitValue(int value) :
        value{value}
    {}

    ForwardLimitValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case ForwardLimitValue::ClosedToGround: return "Closed To Ground";
        case ForwardLimitValue::Open: return "Open";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const ForwardLimitValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const ForwardLimitValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const ForwardLimitValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  Reverse Limit Pin.
 */
class ReverseLimitValue : public ISerializable
{
public:
    int value;

    static constexpr int ClosedToGround = 0;
    static constexpr int Open = 1;

    ReverseLimitValue(int value) :
        value{value}
    {}

    ReverseLimitValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case ReverseLimitValue::ClosedToGround: return "Closed To Ground";
        case ReverseLimitValue::Open: return "Open";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const ReverseLimitValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const ReverseLimitValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const ReverseLimitValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};

/**
 * \brief  The active control mode of the motor controller
 */
class TalonFX_ControlModeValue : public ISerializable
{
public:
    int value;

    static constexpr int DisabledOutput = 0;
    static constexpr int NeutralOut = 1;
    static constexpr int FullBrake = 2;
    static constexpr int DutyCycle_OpenLoop = 3;
    static constexpr int DutyCycle_Position = 4;
    static constexpr int DutyCycle_Velocity = 5;
    static constexpr int DutyCycle_MotionMag = 6;
    static constexpr int DutyCycleFOC_OpenLoop = 7;
    static constexpr int DutyCycleFOC_Position = 8;
    static constexpr int DutyCycleFOC_Velocity = 9;
    static constexpr int DutyCycleFOC_MotionMag = 10;
    static constexpr int Voltage_OpenLoop = 11;
    static constexpr int Voltage_Position = 12;
    static constexpr int Voltage_Velocity = 13;
    static constexpr int Voltage_MotionMag = 14;
    static constexpr int VoltageFOC_OpenLoop = 15;
    static constexpr int VoltageFOC_Position = 16;
    static constexpr int VoltageFOC_Velocity = 17;
    static constexpr int VoltageFOC_MotionMag = 18;
    static constexpr int TorqueCurrent_OpenLoop = 19;
    static constexpr int TorqueCurrent_Position = 20;
    static constexpr int TorqueCurrent_Velocity = 21;
    static constexpr int TorqueCurrent_MotionMag = 22;
    static constexpr int Follower = 23;
    static constexpr int Reserved = 24;

    TalonFX_ControlModeValue(int value) :
        value{value}
    {}

    TalonFX_ControlModeValue() :
        value{-1}
    {}

    /**
     * \brief Gets the string representation of this enum
     *
     * \returns String representation of this enum
     */
    std::string ToString() const
    {
        switch(value)
        {
        case TalonFX_ControlModeValue::DisabledOutput: return "DisabledOutput";
        case TalonFX_ControlModeValue::NeutralOut: return "NeutralOut";
        case TalonFX_ControlModeValue::FullBrake: return "FullBrake";
        case TalonFX_ControlModeValue::DutyCycle_OpenLoop: return "DutyCycle_OpenLoop";
        case TalonFX_ControlModeValue::DutyCycle_Position: return "DutyCycle_Position";
        case TalonFX_ControlModeValue::DutyCycle_Velocity: return "DutyCycle_Velocity";
        case TalonFX_ControlModeValue::DutyCycle_MotionMag: return "DutyCycle_MotionMag";
        case TalonFX_ControlModeValue::DutyCycleFOC_OpenLoop: return "DutyCycleFOC_OpenLoop";
        case TalonFX_ControlModeValue::DutyCycleFOC_Position: return "DutyCycleFOC_Position";
        case TalonFX_ControlModeValue::DutyCycleFOC_Velocity: return "DutyCycleFOC_Velocity";
        case TalonFX_ControlModeValue::DutyCycleFOC_MotionMag: return "DutyCycleFOC_MotionMag";
        case TalonFX_ControlModeValue::Voltage_OpenLoop: return "Voltage_OpenLoop";
        case TalonFX_ControlModeValue::Voltage_Position: return "Voltage_Position";
        case TalonFX_ControlModeValue::Voltage_Velocity: return "Voltage_Velocity";
        case TalonFX_ControlModeValue::Voltage_MotionMag: return "Voltage_MotionMag";
        case TalonFX_ControlModeValue::VoltageFOC_OpenLoop: return "VoltageFOC_OpenLoop";
        case TalonFX_ControlModeValue::VoltageFOC_Position: return "VoltageFOC_Position";
        case TalonFX_ControlModeValue::VoltageFOC_Velocity: return "VoltageFOC_Velocity";
        case TalonFX_ControlModeValue::VoltageFOC_MotionMag: return "VoltageFOC_MotionMag";
        case TalonFX_ControlModeValue::TorqueCurrent_OpenLoop: return "TorqueCurrent_OpenLoop";
        case TalonFX_ControlModeValue::TorqueCurrent_Position: return "TorqueCurrent_Position";
        case TalonFX_ControlModeValue::TorqueCurrent_Velocity: return "TorqueCurrent_Velocity";
        case TalonFX_ControlModeValue::TorqueCurrent_MotionMag: return "TorqueCurrent_MotionMag";
        case TalonFX_ControlModeValue::Follower: return "Follower";
        case TalonFX_ControlModeValue::Reserved: return "Reserved";
        default: return "Invalid Value";
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const TalonFX_ControlModeValue& data)
    {
        os << data.ToString();
        return os;
    }

    std::string Serialize() const
    {
        std::stringstream ss;
        ss << "u_" << this->value;
        return ss.str();
    }

    bool operator==(const TalonFX_ControlModeValue& data) const
    {
        return this->value == data.value;
    }
    bool operator==(int data) const
    {
        return this->value == data;
    }
    bool operator<(const TalonFX_ControlModeValue& data) const
    {
        return this->value < data.value;
    }
    bool operator<(int data) const
    {
        return this->value < data;
    }
};


}
}
}
