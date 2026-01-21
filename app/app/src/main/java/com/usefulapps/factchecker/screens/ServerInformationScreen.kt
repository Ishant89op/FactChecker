package com.usefulapps.factchecker.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.dimensionResource
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.usefulapps.factchecker.R
import com.usefulapps.factchecker.viewmodel.ServerInformationViewModel
import org.koin.androidx.compose.koinViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Preview(showBackground = true)
@Composable
fun ServerInformationScreen(
    modifier: Modifier = Modifier,
    viewModel: ServerInformationViewModel = koinViewModel(),
    closeIconClick: () -> Unit = {}
) {

    val uiState by viewModel.uiState.collectAsState()

    Scaffold(
        modifier = modifier,
        topBar = {
            CenterAlignedTopAppBar(
                title = {
                    Text(
                        text = stringResource(R.string.server_information_app_bar),
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                },
                navigationIcon = {
                    IconButton(
                        onClick = closeIconClick
                    ) {
                        Icon(
                            painter = painterResource(R.drawable.close_small_24),
                            contentDescription = "Close"
                        )
                    }
                }
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            val imageSize = dimensionResource(R.dimen.server_info_images_size)

            val clientImage = painterResource(R.drawable.client_black)

            val syncImage = if(uiState.isServerOnline) {
                painterResource(R.drawable.sync_black)
            } else {
                painterResource(R.drawable.close_small_24)
            }

            val serverImage = if(uiState.isServerOnline) {
                painterResource(R.drawable.host_green)
            } else {
                painterResource(R.drawable.host_red)
            }

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .fillMaxHeight(0.5f),
                horizontalArrangement = Arrangement.SpaceEvenly,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Image(
                    painter = clientImage,
                    contentDescription = stringResource(R.string.client),
                    modifier = Modifier.size(imageSize)
                )
                Image(
                    painter = syncImage,
                    contentDescription = stringResource(R.string.sync),
                    modifier = Modifier.size(imageSize)
                )
                Image(
                    painter = serverImage,
                    contentDescription = stringResource(R.string.host),
                    modifier = Modifier.size(imageSize)
                )
            }
        }
    }
}