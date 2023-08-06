/*
 * Copyright (c) CTR-Electronics
 * Contact support@ctr-electronics for any questions
 * including support, features, and licensing.
 */
#pragma once

#include "ctre/phoenix/export.h"
#include <cstdint>
#include <string>

#ifdef __cplusplus
extern "C"
{
#endif
    CTREXPORT int c_ctre_phoenixpro_requestConfigApply(const char *canbus, uint32_t ecuEncoding, double timeoutSeconds, const char *str, size_t strlen, bool forceApply);
CTREXPORT int c_ctre_phoenixpro_RequestControlDutyCycleOut(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, double Output, bool EnableFOC);
CTREXPORT int c_ctre_phoenixpro_RequestControlTorqueCurrentFOC(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, double Output, double MaxAbsDutyCycle, double Deadband);
CTREXPORT int c_ctre_phoenixpro_RequestControlVoltageOut(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, double Output, bool EnableFOC);
CTREXPORT int c_ctre_phoenixpro_RequestControlPositionDutyCycle(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, double Position, bool EnableFOC, double FeedForward, int Slot);
CTREXPORT int c_ctre_phoenixpro_RequestControlPositionVoltage(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, double Position, bool EnableFOC, double FeedForward, int Slot);
CTREXPORT int c_ctre_phoenixpro_RequestControlPositionTorqueCurrentFOC(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, double Position, double FeedForward, int Slot);
CTREXPORT int c_ctre_phoenixpro_RequestControlVelocityDutyCycle(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, double Velocity, bool EnableFOC, double FeedForward, int Slot);
CTREXPORT int c_ctre_phoenixpro_RequestControlVelocityVoltage(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, double Velocity, bool EnableFOC, double FeedForward, int Slot);
CTREXPORT int c_ctre_phoenixpro_RequestControlVelocityTorqueCurrentFOC(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, double Velocity, double FeedForward, int Slot);
CTREXPORT int c_ctre_phoenixpro_RequestControlMotionMagicDutyCycle(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, double Position, bool EnableFOC, double FeedForward, int Slot);
CTREXPORT int c_ctre_phoenixpro_RequestControlMotionMagicVoltage(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, double Position, bool EnableFOC, double FeedForward, int Slot);
CTREXPORT int c_ctre_phoenixpro_RequestControlMotionMagicTorqueCurrentFOC(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, double Position, double FeedForward, int Slot);
CTREXPORT int c_ctre_phoenixpro_RequestControlFollower(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, int MasterID, bool OpposeMasterDirection);
CTREXPORT int c_ctre_phoenixpro_RequestControlStrictFollower(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, int MasterID);
CTREXPORT int c_ctre_phoenixpro_RequestControlNeutralOut(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests);
CTREXPORT int c_ctre_phoenixpro_RequestControlStaticBrake(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests);
CTREXPORT int c_ctre_phoenixpro_RequestControlBalanceBattery(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests);
CTREXPORT int c_ctre_phoenixpro_RequestControlBMSManualIsolator(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, bool Enable);
CTREXPORT int c_ctre_phoenixpro_RequestControlBMSManualVboost(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, bool EnableClosedLoop, double TargetVoltage, double TargetDutyCycle);
CTREXPORT int c_ctre_phoenixpro_RequestControlBMSManualPwmJunction(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests, int JunctionSelect, double JunctionDutyCycle);
CTREXPORT int c_ctre_phoenixpro_RequestControlBMSClearFault(const char *canbus, uint32_t ecuEncoding, double updateTime, bool cancelOtherRequests);
#ifdef __cplusplus
}
#endif
