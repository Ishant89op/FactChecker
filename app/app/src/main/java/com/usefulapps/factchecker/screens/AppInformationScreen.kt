package com.usefulapps.factchecker.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.Divider
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.usefulapps.factchecker.R
import com.usefulapps.factchecker.ui.theme.bodyFontFamily
import com.usefulapps.factchecker.ui.theme.displayFontFamily

@OptIn(ExperimentalMaterial3Api::class)
@Preview(showBackground = true, showSystemUi = true)
@Composable
fun AppInfoScreen(
    modifier: Modifier = Modifier,
    onClose: () -> Unit = {}
) {
    val context = LocalContext.current
    val versionName = "1.0.0"
    val buildType = "BuildConfig.BUILD_TYPE"
    val appName = stringResource(R.string.app_name)

    Scaffold(
        modifier = modifier
            .padding(20.dp),
        topBar = {
            CenterAlignedTopAppBar(
                title = {
                    Text(
                        text = stringResource(R.string.app_information_app_bar),
                        fontFamily = displayFontFamily
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onClose) {
                        Icon(
                            painter = painterResource(R.drawable.close_small_24),
                            contentDescription = stringResource(R.string.close_button_CD)
                        )
                    }
                }
            )
        }
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            item {
                Spacer(Modifier.height(24.dp))
                Text(
                    text = appName,
                    fontSize = 22.sp,
                    fontWeight = FontWeight.Bold
                )

                Text(
                    text = "Version $versionName ($buildType)",
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )

                Spacer(Modifier.height(24.dp))
                HorizontalDivider()
                Spacer(Modifier.height(24.dp))
            }

            item {
                SectionTitle("What this app does")
                SectionBody(
                    "This app verifies user-provided facts or statements by checking publicly available online sources."
                )
            }

            item {
                Spacer(Modifier.height(24.dp))
                HorizontalDivider()
                Spacer(Modifier.height(24.dp))
            }

            item {
                SectionTitle("Permissions used")
                SectionBody(
                    "• Internet – Required to fetch and verify information from online sources.\n" +
                            "• Network state – Used to ensure connectivity before making requests."
                )
            }

            item {
                Spacer(Modifier.height(24.dp))
                HorizontalDivider()
                Spacer(Modifier.height(24.dp))
            }

            item {
                SectionTitle("Data & accuracy")
                SectionBody(
                    "Results are generated using third-party data sources. Accuracy may vary depending on source availability and context."
                )
            }

            item {
                Spacer(Modifier.height(24.dp))
                Divider()
                Spacer(Modifier.height(24.dp))
            }

            item {
                SectionTitle("Privacy")
                SectionBody(
                    "This app does not store personal data. User input is processed only to perform fact verification."
                )
            }

            item {
                Spacer(Modifier.height(32.dp))

                Text(
                    text = "Use it. Break it. Improvements will follow.",
                    fontStyle = FontStyle.Italic,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}


@Composable
private fun SectionTitle(text: String) {
    Text(
        text = text,
        fontWeight = FontWeight.Bold,
        fontSize = 16.sp,
        fontFamily = bodyFontFamily
    )
}

@Composable
private fun SectionBody(text: String) {
    Spacer(Modifier.height(8.dp))
    Text(
        text = text,
        fontSize = 14.sp,
        fontFamily = bodyFontFamily
    )
}
