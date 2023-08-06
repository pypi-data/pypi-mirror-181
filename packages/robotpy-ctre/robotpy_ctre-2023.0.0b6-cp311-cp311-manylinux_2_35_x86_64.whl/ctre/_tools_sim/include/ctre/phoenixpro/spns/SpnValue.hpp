/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include <string>

namespace ctre
{
    namespace phoenixpro
    {
        namespace spns
        {
            /**
             * \brief Class that holds all the SPN values used in Phoenix Pro devices.
             */
            class SpnValue
            {
            public:
                int value;

                static constexpr int TalonFX_System_State = 611;
                static constexpr int Startup_ResetFlags = 632;
                static constexpr int AbsPosition = 729;
                static constexpr int CANCoder_SupplyVoltage = 730;
                static constexpr int CANcoder_MagHealth = 731;
                static constexpr int CANCoder_PulseWidth = 732;
                static constexpr int Version_Major = 733;
                static constexpr int Version_Minor = 734;
                static constexpr int Version_Bugfix = 735;
                static constexpr int Version_Build = 736;
                static constexpr int Version_Full = 737;
                static constexpr int Licensing_IsProLicensed = 750;
                static constexpr int VoltageRampRate = 823;
                static constexpr int Slot0_kP = 824;
                static constexpr int Slot0_kI = 825;
                static constexpr int Slot0_kD = 826;
                static constexpr int Slot0_kV = 827;
                static constexpr int Slot0_PeakOutput = 830;
                static constexpr int Slot1_kP = 831;
                static constexpr int Slot1_kI = 832;
                static constexpr int Slot1_kD = 833;
                static constexpr int Slot1_kV = 834;
                static constexpr int Slot1_PeakOutput = 837;
                static constexpr int CANcoder_SensorDirection = 839;
                static constexpr int FrcLock = 841;
                static constexpr int RobotEnabled = 842;
                static constexpr int LED1_OnColor = 844;
                static constexpr int LED1_OffColor = 845;
                static constexpr int LED2_OnColor = 846;
                static constexpr int LED2_OffColor = 847;
                static constexpr int Velocity = 889;
                static constexpr int Position = 890;
                static constexpr int Inverted = 919;
                static constexpr int Pigeon2Temperature = 983;
                static constexpr int Pigeon2NoMotionCalEnabled = 984;
                static constexpr int Pigeon2NoMotionCount = 985;
                static constexpr int Pigeon2UpTime = 986;
                static constexpr int Pigeon2TempCompDisabled = 987;
                static constexpr int Pigeon2_SupplyVoltage = 990;
                static constexpr int Pigeon2Yaw = 992;
                static constexpr int Pigeon2Pitch = 993;
                static constexpr int Pigeon2Roll = 994;
                static constexpr int Pigeon2QuatW = 995;
                static constexpr int Pigeon2QuatX = 996;
                static constexpr int Pigeon2QuatY = 997;
                static constexpr int Pigeon2QuatZ = 998;
                static constexpr int Pigeon2AccumGyroX = 999;
                static constexpr int Pigeon2AccumGyroY = 1000;
                static constexpr int Pigeon2AccumGyroZ = 1001;
                static constexpr int Pigeon2GravityVectorX = 1002;
                static constexpr int Pigeon2GravityVectorY = 1003;
                static constexpr int Pigeon2GravityVectorZ = 1004;
                static constexpr int Pigeon2AngularVelocityX = 1005;
                static constexpr int Pigeon2AngularVelocityY = 1006;
                static constexpr int Pigeon2AngularVelocityZ = 1007;
                static constexpr int Pigeon2MagneticFieldX = 1008;
                static constexpr int Pigeon2MagneticFieldY = 1009;
                static constexpr int Pigeon2MagneticFieldZ = 1010;
                static constexpr int Pigeon2AccelerationX = 1011;
                static constexpr int Pigeon2AccelerationY = 1012;
                static constexpr int Pigeon2AccelerationZ = 1013;
                static constexpr int Pigeon2RawMagneticFieldX = 1018;
                static constexpr int Pigeon2RawMagneticFieldY = 1019;
                static constexpr int Pigeon2RawMagneticFieldZ = 1020;
                static constexpr int CANCoder_MagnetOffset = 1021;
                static constexpr int CANcoder_AbsoluteSensorRange = 1022;
                static constexpr int CANCoder_RawPos = 1043;
                static constexpr int CANCoder_RawVel = 1044;
                static constexpr int DeviceEnabled = 1055;
                static constexpr int ForwardLimit = 1380;
                static constexpr int ReverseLimit = 1381;
                static constexpr int PRO_MotorOutput_DutyCycle = 1383;
                static constexpr int PRO_MotorOutput_TorqueCurrent = 1385;
                static constexpr int PRO_SupplyAndTemp_StatorCurrent = 1386;
                static constexpr int PRO_SupplyAndTemp_SupplyCurrent = 1387;
                static constexpr int PRO_SupplyAndTemp_SupplyVoltage = 1388;
                static constexpr int PRO_SupplyAndTemp_DeviceTemp = 1389;
                static constexpr int PRO_SupplyAndTemp_ProcessorTemp = 1390;
                static constexpr int PRO_PosAndVel_Velocity = 1396;
                static constexpr int PRO_PosAndVel_Position = 1397;
                static constexpr int PRO_PIDStateEnables_IntegratedAccum_DC = 1398;
                static constexpr int PRO_PIDStateEnables_IntegratedAccum_V = 1399;
                static constexpr int PRO_PIDStateEnables_IntegratedAccum_A = 1400;
                static constexpr int PRO_PIDStateEnables_FeedForward_DC = 1401;
                static constexpr int PRO_PIDStateEnables_FeedForward_V = 1402;
                static constexpr int PRO_PIDStateEnables_FeedForward_A = 1403;
                static constexpr int TalonFX_ControlMode = 1404;
                static constexpr int PRO_PIDRefPIDErr_PIDRef_Position = 1409;
                static constexpr int PRO_PIDRefPIDErr_PIDRef_Velocity = 1410;
                static constexpr int PRO_PIDRefPIDErr_PIDErr_Position = 1411;
                static constexpr int PRO_PIDRefPIDErr_PIDErr_Velocity = 1412;
                static constexpr int PRO_PIDOutput_ProportionalOutput_DC = 1414;
                static constexpr int PRO_PIDOutput_ProportionalOutput_V = 1415;
                static constexpr int PRO_PIDOutput_ProportionalOutput_A = 1416;
                static constexpr int PRO_PIDOutput_DerivativeOutput_DC = 1417;
                static constexpr int PRO_PIDOutput_DerivativeOutput_V = 1418;
                static constexpr int PRO_PIDOutput_DerivativeOutput_A = 1419;
                static constexpr int PRO_PIDOutput_Output_DC = 1420;
                static constexpr int PRO_PIDOutput_Output_V = 1421;
                static constexpr int PRO_PIDOutput_Output_A = 1422;
                static constexpr int PRO_PIDOutput_Slot = 1423;
                static constexpr int PRO_PIDRefSlopeECUTime_ReferenceSlope_Position = 1424;
                static constexpr int PRO_PIDRefSlopeECUTime_ReferenceSlope_Velocity = 1425;
                static constexpr int SupplyVoltageLowpassTimeConstant = 1427;

                /**
                 * \brief Gets the string representation of this enum
                 *
                 * \returns String representation of this enum
                 */
                std::string ToString() const
                {
                    switch (value)
                    {
                    case SpnValue::TalonFX_System_State: return "TalonFX_System_State";
                    case SpnValue::Startup_ResetFlags: return "Startup_ResetFlags";
                    case SpnValue::AbsPosition: return "AbsPosition";
                    case SpnValue::CANCoder_SupplyVoltage: return "CANCoder_SupplyVoltage";
                    case SpnValue::CANcoder_MagHealth: return "CANcoder_MagHealth";
                    case SpnValue::CANCoder_PulseWidth: return "CANCoder_PulseWidth";
                    case SpnValue::Version_Major: return "Version_Major";
                    case SpnValue::Version_Minor: return "Version_Minor";
                    case SpnValue::Version_Bugfix: return "Version_Bugfix";
                    case SpnValue::Version_Build: return "Version_Build";
                    case SpnValue::Version_Full: return "Version_Full";
                    case SpnValue::Licensing_IsProLicensed: return "Licensing_IsProLicensed";
                    case SpnValue::VoltageRampRate: return "VoltageRampRate";
                    case SpnValue::Slot0_kP: return "Slot0_kP";
                    case SpnValue::Slot0_kI: return "Slot0_kI";
                    case SpnValue::Slot0_kD: return "Slot0_kD";
                    case SpnValue::Slot0_kV: return "Slot0_kV";
                    case SpnValue::Slot0_PeakOutput: return "Slot0_PeakOutput";
                    case SpnValue::Slot1_kP: return "Slot1_kP";
                    case SpnValue::Slot1_kI: return "Slot1_kI";
                    case SpnValue::Slot1_kD: return "Slot1_kD";
                    case SpnValue::Slot1_kV: return "Slot1_kV";
                    case SpnValue::Slot1_PeakOutput: return "Slot1_PeakOutput";
                    case SpnValue::CANcoder_SensorDirection: return "CANcoder_SensorDirection";
                    case SpnValue::FrcLock: return "FrcLock";
                    case SpnValue::RobotEnabled: return "RobotEnabled";
                    case SpnValue::LED1_OnColor: return "LED1_OnColor";
                    case SpnValue::LED1_OffColor: return "LED1_OffColor";
                    case SpnValue::LED2_OnColor: return "LED2_OnColor";
                    case SpnValue::LED2_OffColor: return "LED2_OffColor";
                    case SpnValue::Velocity: return "Velocity";
                    case SpnValue::Position: return "Position";
                    case SpnValue::Inverted: return "Inverted";
                    case SpnValue::Pigeon2Temperature: return "Pigeon2Temperature";
                    case SpnValue::Pigeon2NoMotionCalEnabled: return "Pigeon2NoMotionCalEnabled";
                    case SpnValue::Pigeon2NoMotionCount: return "Pigeon2NoMotionCount";
                    case SpnValue::Pigeon2UpTime: return "Pigeon2UpTime";
                    case SpnValue::Pigeon2TempCompDisabled: return "Pigeon2TempCompDisabled";
                    case SpnValue::Pigeon2_SupplyVoltage: return "Pigeon2_SupplyVoltage";
                    case SpnValue::Pigeon2Yaw: return "Pigeon2Yaw";
                    case SpnValue::Pigeon2Pitch: return "Pigeon2Pitch";
                    case SpnValue::Pigeon2Roll: return "Pigeon2Roll";
                    case SpnValue::Pigeon2QuatW: return "Pigeon2QuatW";
                    case SpnValue::Pigeon2QuatX: return "Pigeon2QuatX";
                    case SpnValue::Pigeon2QuatY: return "Pigeon2QuatY";
                    case SpnValue::Pigeon2QuatZ: return "Pigeon2QuatZ";
                    case SpnValue::Pigeon2AccumGyroX: return "Pigeon2AccumGyroX";
                    case SpnValue::Pigeon2AccumGyroY: return "Pigeon2AccumGyroY";
                    case SpnValue::Pigeon2AccumGyroZ: return "Pigeon2AccumGyroZ";
                    case SpnValue::Pigeon2GravityVectorX: return "Pigeon2GravityVectorX";
                    case SpnValue::Pigeon2GravityVectorY: return "Pigeon2GravityVectorY";
                    case SpnValue::Pigeon2GravityVectorZ: return "Pigeon2GravityVectorZ";
                    case SpnValue::Pigeon2AngularVelocityX: return "Pigeon2AngularVelocityX";
                    case SpnValue::Pigeon2AngularVelocityY: return "Pigeon2AngularVelocityY";
                    case SpnValue::Pigeon2AngularVelocityZ: return "Pigeon2AngularVelocityZ";
                    case SpnValue::Pigeon2MagneticFieldX: return "Pigeon2MagneticFieldX";
                    case SpnValue::Pigeon2MagneticFieldY: return "Pigeon2MagneticFieldY";
                    case SpnValue::Pigeon2MagneticFieldZ: return "Pigeon2MagneticFieldZ";
                    case SpnValue::Pigeon2AccelerationX: return "Pigeon2AccelerationX";
                    case SpnValue::Pigeon2AccelerationY: return "Pigeon2AccelerationY";
                    case SpnValue::Pigeon2AccelerationZ: return "Pigeon2AccelerationZ";
                    case SpnValue::Pigeon2RawMagneticFieldX: return "Pigeon2RawMagneticFieldX";
                    case SpnValue::Pigeon2RawMagneticFieldY: return "Pigeon2RawMagneticFieldY";
                    case SpnValue::Pigeon2RawMagneticFieldZ: return "Pigeon2RawMagneticFieldZ";
                    case SpnValue::CANCoder_MagnetOffset: return "CANCoder_MagnetOffset";
                    case SpnValue::CANcoder_AbsoluteSensorRange: return "CANcoder_AbsoluteSensorRange";
                    case SpnValue::CANCoder_RawPos: return "CANCoder_RawPos";
                    case SpnValue::CANCoder_RawVel: return "CANCoder_RawVel";
                    case SpnValue::DeviceEnabled: return "DeviceEnabled";
                    case SpnValue::ForwardLimit: return "ForwardLimit";
                    case SpnValue::ReverseLimit: return "ReverseLimit";
                    case SpnValue::PRO_MotorOutput_DutyCycle: return "PRO_MotorOutput_DutyCycle";
                    case SpnValue::PRO_MotorOutput_TorqueCurrent: return "PRO_MotorOutput_TorqueCurrent";
                    case SpnValue::PRO_SupplyAndTemp_StatorCurrent: return "PRO_SupplyAndTemp_StatorCurrent";
                    case SpnValue::PRO_SupplyAndTemp_SupplyCurrent: return "PRO_SupplyAndTemp_SupplyCurrent";
                    case SpnValue::PRO_SupplyAndTemp_SupplyVoltage: return "PRO_SupplyAndTemp_SupplyVoltage";
                    case SpnValue::PRO_SupplyAndTemp_DeviceTemp: return "PRO_SupplyAndTemp_DeviceTemp";
                    case SpnValue::PRO_SupplyAndTemp_ProcessorTemp: return "PRO_SupplyAndTemp_ProcessorTemp";
                    case SpnValue::PRO_PosAndVel_Velocity: return "PRO_PosAndVel_Velocity";
                    case SpnValue::PRO_PosAndVel_Position: return "PRO_PosAndVel_Position";
                    case SpnValue::PRO_PIDStateEnables_IntegratedAccum_DC: return "PRO_PIDStateEnables_IntegratedAccum_DC";
                    case SpnValue::PRO_PIDStateEnables_IntegratedAccum_V: return "PRO_PIDStateEnables_IntegratedAccum_V";
                    case SpnValue::PRO_PIDStateEnables_IntegratedAccum_A: return "PRO_PIDStateEnables_IntegratedAccum_A";
                    case SpnValue::PRO_PIDStateEnables_FeedForward_DC: return "PRO_PIDStateEnables_FeedForward_DC";
                    case SpnValue::PRO_PIDStateEnables_FeedForward_V: return "PRO_PIDStateEnables_FeedForward_V";
                    case SpnValue::PRO_PIDStateEnables_FeedForward_A: return "PRO_PIDStateEnables_FeedForward_A";
                    case SpnValue::TalonFX_ControlMode: return "TalonFX_ControlMode";
                    case SpnValue::PRO_PIDRefPIDErr_PIDRef_Position: return "PRO_PIDRefPIDErr_PIDRef_Position";
                    case SpnValue::PRO_PIDRefPIDErr_PIDRef_Velocity: return "PRO_PIDRefPIDErr_PIDRef_Velocity";
                    case SpnValue::PRO_PIDRefPIDErr_PIDErr_Position: return "PRO_PIDRefPIDErr_PIDErr_Position";
                    case SpnValue::PRO_PIDRefPIDErr_PIDErr_Velocity: return "PRO_PIDRefPIDErr_PIDErr_Velocity";
                    case SpnValue::PRO_PIDOutput_ProportionalOutput_DC: return "PRO_PIDOutput_ProportionalOutput_DC";
                    case SpnValue::PRO_PIDOutput_ProportionalOutput_V: return "PRO_PIDOutput_ProportionalOutput_V";
                    case SpnValue::PRO_PIDOutput_ProportionalOutput_A: return "PRO_PIDOutput_ProportionalOutput_A";
                    case SpnValue::PRO_PIDOutput_DerivativeOutput_DC: return "PRO_PIDOutput_DerivativeOutput_DC";
                    case SpnValue::PRO_PIDOutput_DerivativeOutput_V: return "PRO_PIDOutput_DerivativeOutput_V";
                    case SpnValue::PRO_PIDOutput_DerivativeOutput_A: return "PRO_PIDOutput_DerivativeOutput_A";
                    case SpnValue::PRO_PIDOutput_Output_DC: return "PRO_PIDOutput_Output_DC";
                    case SpnValue::PRO_PIDOutput_Output_V: return "PRO_PIDOutput_Output_V";
                    case SpnValue::PRO_PIDOutput_Output_A: return "PRO_PIDOutput_Output_A";
                    case SpnValue::PRO_PIDOutput_Slot: return "PRO_PIDOutput_Slot";
                    case SpnValue::PRO_PIDRefSlopeECUTime_ReferenceSlope_Position: return "PRO_PIDRefSlopeECUTime_ReferenceSlope_Position";
                    case SpnValue::PRO_PIDRefSlopeECUTime_ReferenceSlope_Velocity: return "PRO_PIDRefSlopeECUTime_ReferenceSlope_Velocity";
                    case SpnValue::SupplyVoltageLowpassTimeConstant: return "SupplyVoltageLowpassTimeConstant";
                    default:
                        return "Invalid Value";
                    }
                }

                friend std::ostream &operator<<(std::ostream &os, const SpnValue &data)
                {
                    os << data.ToString();
                    return os;
                }
                bool operator==(const SpnValue &data) const
                {
                    return this->value == data.value;
                }
                bool operator==(int data) const
                {
                    return this->value == data;
                }
                bool operator<(const SpnValue &data) const
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
