package com.usefulapps.factchecker

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.usefulapps.factchecker.screens.HomeScreen
import com.usefulapps.factchecker.ui.theme.FactCheckerTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            FactCheckerTheme {
                FactChecker()
            }
        }
    }
}

@Composable
fun FactChecker(modifier: Modifier = Modifier) {
    HomeScreen()
}
