package com.usefulapps.factchecker.navigation

import kotlinx.serialization.Serializable

sealed interface Route {
    @Serializable
    data object HomeScreen : Route

    @Serializable
    data object ResultScreen : Route

    @Serializable
    data object HistoryScreen : Route

    @Serializable
    data object SettingsScreen : Route

    @Serializable
    data object ServerInformationScreen : Route
}