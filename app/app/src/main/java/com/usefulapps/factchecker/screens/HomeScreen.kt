package com.usefulapps.factchecker.screens

import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.usefulapps.factchecker.ui.theme.*
import com.usefulapps.factchecker.viewmodel.HomeViewModel
import org.koin.androidx.compose.koinViewModel

@Composable
fun HomeScreen(
    modifier: Modifier = Modifier,
    viewModel: HomeViewModel = koinViewModel(),
    onNavigateToResult: () -> Unit = {},
    onNavigateToHistory: () -> Unit = {},
    onNavigateToSettings: () -> Unit = {},
    onServerInfoClick: () -> Unit = {}
) {
    val uiState by viewModel.uiState.collectAsState()

    // Navigate to result screen when result arrives
    LaunchedEffect(uiState.showResults) {
        if (uiState.showResults && uiState.result != null) {
            onNavigateToResult()
        }
    }

    Scaffold(
        bottomBar = {
            BottomNavBar(
                selected = 0,
                onHomeClick = {},
                onHistoryClick = onNavigateToHistory,
                onSettingsClick = onNavigateToSettings
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        if (uiState.isLoading) {
            // Loading state - matches Stitch loading design
            LoadingView(
                modifier = Modifier.padding(padding),
                status = uiState.currentStatus,
                message = uiState.statusMessage,
                sourcesChecked = uiState.sourcesChecked
            )
        } else {
            Column(
                modifier = Modifier
                    .padding(padding)
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
            ) {
                // Top App Bar
                TopBar()

                // Hero Section
                Column(modifier = Modifier.padding(horizontal = 24.dp, vertical = 16.dp)) {
                    Text(
                        text = "Verify claims.\nTrust sources.",
                        style = MaterialTheme.typography.displaySmall.copy(
                            fontWeight = FontWeight.Bold,
                            fontStyle = FontStyle.Italic,
                            lineHeight = 40.sp
                        ),
                        color = MaterialTheme.colorScheme.primary
                    )

                    Spacer(modifier = Modifier.height(12.dp))

                    Text(
                        text = "In an age of rapid information, ensure the integrity of what you read. Our AI-driven engine cross-references verified archives in seconds.",
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }

                Spacer(modifier = Modifier.height(16.dp))

                // Input Card
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 24.dp),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.surfaceContainerLow
                    ),
                    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                ) {
                    Column(modifier = Modifier.padding(8.dp)) {
                        OutlinedTextField(
                            value = uiState.input,
                            onValueChange = viewModel::setInput,
                            modifier = Modifier
                                .fillMaxWidth()
                                .heightIn(min = 160.dp),
                            placeholder = {
                                Text(
                                    "Paste a claim, article link, or statement here to verify...",
                                    color = MaterialTheme.colorScheme.outline
                                )
                            },
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedBorderColor = Color.Transparent,
                                unfocusedBorderColor = Color.Transparent,
                                focusedContainerColor = Color.Transparent,
                                unfocusedContainerColor = Color.Transparent,
                            ),
                            enabled = uiState.isInputEnabled
                        )

                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(8.dp),
                            horizontalArrangement = Arrangement.End
                        ) {
                            Button(
                                onClick = { viewModel.verify() },
                                enabled = uiState.input.isNotBlank() && uiState.isInputEnabled,
                                modifier = Modifier.height(52.dp),
                                shape = RoundedCornerShape(12.dp),
                                colors = ButtonDefaults.buttonColors(
                                    containerColor = MaterialTheme.colorScheme.primary
                                )
                            ) {
                                Text(
                                    "Verify",
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 16.sp
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Icon(
                                    Icons.AutoMirrored.Filled.ArrowForward,
                                    contentDescription = null,
                                    modifier = Modifier.size(20.dp)
                                )
                            }
                        }
                    }
                }

                // Error display
                if (uiState.error != null && !uiState.isLoading) {
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(24.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.errorContainer
                        ),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Text(
                            text = uiState.error ?: "",
                            modifier = Modifier.padding(16.dp),
                            color = MaterialTheme.colorScheme.onErrorContainer
                        )
                    }
                }

                Spacer(modifier = Modifier.height(24.dp))

                // Deep Context Engine card
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 24.dp),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(
                        containerColor = Color(0xFFFFDBD1) // primary-fixed
                    )
                ) {
                    Column(modifier = Modifier.padding(24.dp)) {
                        Text(
                            "✨",
                            fontSize = 32.sp
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        Text(
                            "Deep Context Engine",
                            style = MaterialTheme.typography.headlineSmall.copy(
                                fontWeight = FontWeight.Bold
                            ),
                            color = Color(0xFF3A0A00)
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            "We don't just flag \"True\" or \"False\". Our engine analyzes cultural nuances, historical context, and source credibility to give you the complete picture.",
                            style = MaterialTheme.typography.bodyMedium,
                            color = Color(0xFF842503)
                        )
                    }
                }

                Spacer(modifier = Modifier.height(80.dp))
            }
        }
    }
}

@Composable
fun TopBar() {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp, vertical = 16.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(
            text = "FactCheck",
            style = MaterialTheme.typography.headlineMedium.copy(
                fontWeight = FontWeight.Bold,
                fontStyle = FontStyle.Italic
            ),
            color = MaterialTheme.colorScheme.primary
        )
    }
}

@Composable
fun LoadingView(
    modifier: Modifier = Modifier,
    status: String,
    message: String,
    sourcesChecked: Int
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            "Analyzing Authenticity",
            style = MaterialTheme.typography.headlineMedium.copy(
                fontWeight = FontWeight.ExtraBold
            ),
            color = MaterialTheme.colorScheme.onSurface
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            message.ifEmpty { "Initializing..." },
            style = MaterialTheme.typography.bodyLarge.copy(fontStyle = FontStyle.Italic),
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        Spacer(modifier = Modifier.height(24.dp))

        LinearProgressIndicator(
            modifier = Modifier
                .width(200.dp)
                .clip(RoundedCornerShape(2.dp)),
            color = MaterialTheme.colorScheme.primary,
            trackColor = MaterialTheme.colorScheme.outlineVariant
        )

        Spacer(modifier = Modifier.height(48.dp))

        // Status cards
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Web Sources card
            Card(
                modifier = Modifier.weight(1f),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.surfaceContainerLow
                )
            ) {
                Column(modifier = Modifier.padding(20.dp)) {
                    Text(
                        "Web Sources",
                        style = MaterialTheme.typography.titleMedium.copy(
                            fontWeight = FontWeight.Bold,
                            fontStyle = FontStyle.Italic
                        )
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    StatusRow("Playwright", if (status == "scraping") "Scanning" else if (status == "analyzing" || status == "reconciling" || status == "complete") "Done" else "Queued")
                    StatusRow("Sources", if (sourcesChecked > 0) "$sourcesChecked found" else "Waiting")
                }
            }

            // AI Analysis card
            Card(
                modifier = Modifier.weight(1f),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.surfaceContainerHighest
                )
            ) {
                Column(modifier = Modifier.padding(20.dp)) {
                    Text(
                        "AI Analysis",
                        style = MaterialTheme.typography.titleMedium.copy(
                            fontWeight = FontWeight.Bold,
                            fontStyle = FontStyle.Italic
                        )
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    StatusRow("Gemini", if (status == "analyzing") "Running" else if (status == "reconciling" || status == "complete") "Done" else "Queued")
                    StatusRow("OpenAI", if (status == "analyzing") "Running" else if (status == "reconciling" || status == "complete") "Done" else "Queued")
                }
            }
        }
    }
}

@Composable
fun StatusRow(label: String, status: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(
            label,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            status,
            style = MaterialTheme.typography.labelSmall.copy(fontWeight = FontWeight.Bold),
            color = if (status == "Done") MaterialTheme.colorScheme.tertiary
            else if (status == "Scanning" || status == "Running") MaterialTheme.colorScheme.primary
            else MaterialTheme.colorScheme.outline
        )
    }
}

@Composable
fun BottomNavBar(
    selected: Int,
    onHomeClick: () -> Unit,
    onHistoryClick: () -> Unit,
    onSettingsClick: () -> Unit
) {
    NavigationBar(
        containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.95f),
        tonalElevation = 0.dp
    ) {
        NavigationBarItem(
            selected = selected == 0,
            onClick = onHomeClick,
            icon = {
                Icon(Icons.Default.Search, contentDescription = "Home")
            },
            label = { Text("HOME", fontSize = 10.sp, fontWeight = FontWeight.Bold) },
            colors = NavigationBarItemDefaults.colors(
                selectedIconColor = Color(0xFF360F04),
                indicatorColor = Color(0xFFFFDBD1)
            )
        )
        NavigationBarItem(
            selected = selected == 1,
            onClick = onHistoryClick,
            icon = {
                Icon(Icons.Default.Search, contentDescription = "History")
            },
            label = { Text("HISTORY", fontSize = 10.sp) },
            colors = NavigationBarItemDefaults.colors(
                selectedIconColor = Color(0xFF360F04),
                indicatorColor = Color(0xFFFFDBD1)
            )
        )
        NavigationBarItem(
            selected = selected == 2,
            onClick = onSettingsClick,
            icon = {
                Icon(Icons.Default.Search, contentDescription = "Settings")
            },
            label = { Text("SETTINGS", fontSize = 10.sp) },
            colors = NavigationBarItemDefaults.colors(
                selectedIconColor = Color(0xFF360F04),
                indicatorColor = Color(0xFFFFDBD1)
            )
        )
    }
}