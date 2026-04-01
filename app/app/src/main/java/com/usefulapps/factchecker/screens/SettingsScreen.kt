package com.usefulapps.factchecker.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.usefulapps.factchecker.data.remote.HTTPclient
import com.usefulapps.factchecker.viewmodel.HomeViewModel
import org.koin.androidx.compose.koinViewModel

@Composable
fun SettingsScreen(
    modifier: Modifier = Modifier,
    viewModel: HomeViewModel = koinViewModel(),
    onNavigateToHome: () -> Unit = {},
    onNavigateToHistory: () -> Unit = {}
) {
    var backendUrl by remember { mutableStateOf(HTTPclient.baseUrl) }
    var apiKey by remember { mutableStateOf(HTTPclient.apiKey) }

    Scaffold(
        bottomBar = {
            BottomNavBar(
                selected = 2,
                onHomeClick = onNavigateToHome,
                onHistoryClick = onNavigateToHistory,
                onSettingsClick = {}
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
        ) {
            TopBar()

            Column(modifier = Modifier.padding(horizontal = 24.dp)) {
                Text(
                    "Settings",
                    style = MaterialTheme.typography.displaySmall.copy(
                        fontWeight = FontWeight.Bold
                    ),
                    color = MaterialTheme.colorScheme.primary
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    "Configure your verification engine.",
                    style = MaterialTheme.typography.bodyLarge.copy(
                        fontStyle = FontStyle.Italic
                    ),
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            Spacer(modifier = Modifier.height(32.dp))

            // Backend URL Section
            SettingsSection(title = "Backend Connection") {
                OutlinedTextField(
                    value = backendUrl,
                    onValueChange = { backendUrl = it },
                    label = { Text("Backend URL") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    shape = RoundedCornerShape(12.dp)
                )

                Spacer(modifier = Modifier.height(12.dp))

                OutlinedTextField(
                    value = apiKey,
                    onValueChange = { apiKey = it },
                    label = { Text("API Key (X-API-Key)") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    shape = RoundedCornerShape(12.dp)
                )

                Spacer(modifier = Modifier.height(16.dp))

                Button(
                    onClick = {
                        HTTPclient.baseUrl = backendUrl.trimEnd('/')
                        HTTPclient.apiKey = apiKey
                        viewModel.testServer()
                    },
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.primary
                    )
                ) {
                    Text("Save & Test Connection", fontWeight = FontWeight.Bold)
                }
            }

            // Server Status
            val uiState by viewModel.uiState.collectAsState()
            SettingsSection(title = "Server Status") {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Connection", style = MaterialTheme.typography.bodyLarge)
                    Surface(
                        shape = RoundedCornerShape(8.dp),
                        color = if (uiState.isServerOnline)
                            com.usefulapps.factchecker.ui.theme.VerdictTrue.copy(alpha = 0.15f)
                        else
                            com.usefulapps.factchecker.ui.theme.VerdictFalse.copy(alpha = 0.15f)
                    ) {
                        Text(
                            if (uiState.isServerOnline) "ONLINE" else "OFFLINE",
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
                            style = MaterialTheme.typography.labelSmall.copy(
                                fontWeight = FontWeight.Bold,
                                letterSpacing = 1.sp
                            ),
                            color = if (uiState.isServerOnline)
                                com.usefulapps.factchecker.ui.theme.VerdictTrue
                            else
                                com.usefulapps.factchecker.ui.theme.VerdictFalse
                        )
                    }
                }
            }

            // About
            SettingsSection(title = "About FactCheck") {
                Text(
                    "A curated archival tool for the age of information density. Built on the principles of transparency, rigor, and editorial integrity.",
                    style = MaterialTheme.typography.bodyMedium.copy(
                        fontStyle = FontStyle.Italic
                    ),
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(12.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Surface(
                        shape = RoundedCornerShape(20.dp),
                        color = MaterialTheme.colorScheme.surfaceContainerHigh
                    ) {
                        Text(
                            "v3.0.0",
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
                            style = MaterialTheme.typography.labelSmall
                        )
                    }
                    Surface(
                        shape = RoundedCornerShape(20.dp),
                        color = MaterialTheme.colorScheme.surfaceContainerHigh
                    ) {
                        Text(
                            "Model 3 Engine",
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
                            style = MaterialTheme.typography.labelSmall
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(80.dp))
        }
    }
}

@Composable
fun SettingsSection(title: String, content: @Composable ColumnScope.() -> Unit) {
    Column(modifier = Modifier.padding(horizontal = 24.dp, vertical = 12.dp)) {
        Text(
            title,
            style = MaterialTheme.typography.titleLarge.copy(
                fontWeight = FontWeight.Bold
            ),
            color = MaterialTheme.colorScheme.onSurface
        )
        Spacer(modifier = Modifier.height(12.dp))
        content()
    }
}
