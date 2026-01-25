package com.usefulapps.factchecker.navigation

import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.remember
import androidx.navigation3.runtime.entryProvider
import androidx.navigation3.ui.NavDisplay
import com.usefulapps.factchecker.screens.HomeScreen
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
                    onServerInfoClick = { backStack.add(Route.ServerInformationScreen) }
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