package com.usefulapps.factchecker.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material3.Button
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DrawerValue
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalDrawerSheet
import androidx.compose.material3.ModalNavigationDrawer
import androidx.compose.material3.NavigationDrawerItem
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.rememberDrawerState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.usefulapps.factchecker.R
import com.usefulapps.factchecker.data.model.Result
import com.usefulapps.factchecker.viewmodel.HomeViewModel
import kotlinx.coroutines.launch
import org.koin.androidx.compose.koinViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
@Preview(showBackground = true, showSystemUi = true)
fun HomeScreen(
    modifier: Modifier = Modifier,
    viewModel: HomeViewModel = koinViewModel(),
    onAppInfoClick: () -> Unit = {},
    onSettingsClick: () -> Unit = {},
    onHowItWorksClick: () -> Unit = {},
    onServerInfoClick: () -> Unit = {}
) {
    val uiState by viewModel.uiState.collectAsState()

    val drawerState = rememberDrawerState(DrawerValue.Closed)
    val scope = rememberCoroutineScope()

    val serverIcon = painterResource(
        if(uiState.isServerOnline) {
            R.drawable.host_green
        } else {
            R.drawable.host_red
        }
    )

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            DrawerContent(
                modifier = Modifier,
                onAppInfoClick = onAppInfoClick,
                onSettingsClick = onSettingsClick,
                onHowItWorksClick = onHowItWorksClick
            )
        }
    ) {
        Scaffold(
            modifier = modifier,
            topBar = {
                CenterAlignedTopAppBar(
                    title = { Text("Dashboard") },
                    navigationIcon = {
                        IconButton(
                            onClick = {
                                scope.launch {
                                    if(drawerState.isClosed) {
                                        drawerState.open()
                                    } else {
                                        drawerState.close()
                                    }
                                }
                            }
                        ) {
                            Icon(Icons.Default.Menu, contentDescription = "Menu")
                        }
                    },
                    actions = {
                        IconButton(
                            onClick = onServerInfoClick
                        ) {
                            Icon(
                                painter = serverIcon,
                                contentDescription = "Server Online or Not Icon"
                            )
                        }
                    }
                )
            }

        ) { padding ->
            Column(
                modifier = modifier.padding(padding),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                FieldAndButtons(
                    fieldEnabled = uiState.isInputEnabled,
                    checkButtonEnabled = uiState.isCheckButtonEnabled,
                    getInfoButtonEnabled = uiState.isGetInfoButtonEnabled,
                    text = uiState.input,
                    setInformation = viewModel::setInput,
                    check = viewModel::check,
                    getInfo = viewModel::getInfo
                )
                if (uiState.isLoading) Loading()
                if (uiState.showResults) {
                    val errorMessage = uiState.error
                    if (errorMessage != null) {
                        Error(message = errorMessage)
                    } else {
                        Results(uiState.results)
                    }
                }
            }
        }
    }
}

@Composable
@Preview(showBackground = true)
fun FieldAndButtons(
    modifier: Modifier = Modifier,
    text: String = "Write here bro!",
    fieldEnabled: Boolean = true,
    checkButtonEnabled: Boolean = true,
    getInfoButtonEnabled: Boolean = true,
    setInformation: (String) -> Unit = {},
    check: () -> Unit = {},
    getInfo: () -> Unit = {}
) {
    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        OutlinedTextField(
            modifier = Modifier.padding(4.dp),
            value = text,
            onValueChange = setInformation,
            label = {Text(stringResource(R.string.input_field_label))},
            enabled = fieldEnabled
        )

        Row(
            modifier = Modifier,
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceAround
        ) {
            Button(
                modifier = Modifier.padding(8.dp),
                onClick = check,
                enabled = checkButtonEnabled
            ) {
                Text(stringResource(R.string.check_button))
            }

            Button(
                modifier = Modifier.padding(8.dp),
                onClick = getInfo,
                enabled = getInfoButtonEnabled
            ) {
                Text(stringResource(R.string.getInfo_button))
            }
        }
    }
}

@Composable
@Preview(showBackground = true, showSystemUi = true)
fun DrawerContent(
    modifier: Modifier = Modifier,
    onAppInfoClick: () -> Unit = {},
    onSettingsClick: () -> Unit = {},
    onHowItWorksClick: () -> Unit = {}
) {
    ModalDrawerSheet {
        Text(
            text = "App Menu",
            modifier = Modifier.padding(16.dp),
            style = MaterialTheme.typography.titleLarge
        )

        NavigationDrawerItem(
            label = { Text("App Info") },
            selected = true,
            onClick = onAppInfoClick
        )

        NavigationDrawerItem(
            label = { Text("How it works?") },
            selected = false,
            onClick = onHowItWorksClick
        )

        NavigationDrawerItem(
            label = { Text("Settings") },
            selected = false,
            onClick = onSettingsClick
        )
    }
}

@Composable
@Preview(showBackground = true)
fun Loading(
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        CircularProgressIndicator()
    }
}

@Composable
@Preview(showBackground = true)
fun Error(
    modifier: Modifier = Modifier,
    message: String = "Code Red!"
) {
    Column(
        modifier = modifier
    ) {
        Text(message)
    }
}

@Composable
@Preview(showBackground = true)
fun Results(
    results: List<Result>? = null
) {
    Column(
        modifier = Modifier
    ) {
        if (results != null) {
            for(res in results) {
                Text(res.site)
                if(res.found) {
                    Text("Found!")
                    Text(res.url)
                    Text(res.snippet)
                } else {
                    Text("Not Found!")
                }
                Text(res.verdict.toString())
            }
        }
    }
}