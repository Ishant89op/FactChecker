package com.usefulapps.factchecker.navigation

import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.remember
import androidx.navigation3.runtime.entryProvider
import androidx.navigation3.ui.NavDisplay
import com.usefulapps.factchecker.screens.HomeScreen
import com.usefulapps.factchecker.screens.ResultScreen
import com.usefulapps.factchecker.screens.HistoryScreen
import com.usefulapps.factchecker.screens.SettingsScreen
import com.usefulapps.factchecker.screens.ServerInformationScreen

@Composable
fun AppNavigation() {
    val backStack = remember { mutableStateListOf<Any>(Route.HomeScreen) }

    NavDisplay(
        backStack = backStack,
        onBack = { backStack.removeLastOrNull() },
        entryProvider = entryProvider {
            entry<Route.HomeScreen> {
                HomeScreen(
                    onNavigateToResult = { backStack.add(Route.ResultScreen) },
                    onNavigateToHistory = {
                        backStack.clear()
                        backStack.add(Route.HistoryScreen)
                    },
                    onNavigateToSettings = {
                        backStack.clear()
                        backStack.add(Route.SettingsScreen)
                    },
                    onServerInfoClick = { backStack.add(Route.ServerInformationScreen) }
                )
            }

            entry<Route.ResultScreen> {
                ResultScreen(
                    onBackToHome = {
                        backStack.clear()
                        backStack.add(Route.HomeScreen)
                    },
                    onNavigateToHistory = {
                        backStack.clear()
                        backStack.add(Route.HistoryScreen)
                    },
                    onNavigateToSettings = {
                        backStack.clear()
                        backStack.add(Route.SettingsScreen)
                    }
                )
            }

            entry<Route.HistoryScreen> {
                HistoryScreen(
                    onNavigateToHome = {
                        backStack.clear()
                        backStack.add(Route.HomeScreen)
                    },
                    onNavigateToSettings = {
                        backStack.clear()
                        backStack.add(Route.SettingsScreen)
                    }
                )
            }

            entry<Route.SettingsScreen> {
                SettingsScreen(
                    onNavigateToHome = {
                        backStack.clear()
                        backStack.add(Route.HomeScreen)
                    },
                    onNavigateToHistory = {
                        backStack.clear()
                        backStack.add(Route.HistoryScreen)
                    }
                )
            }

            entry<Route.ServerInformationScreen> {
                ServerInformationScreen(
                    closeIconClick = { backStack.removeLastOrNull() }
                )
            }
        }
    )
}