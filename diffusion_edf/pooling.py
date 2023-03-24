from typing import Tuple, List, Dict, Optional, Union

import torch
from torch_cluster import radius_graph, radius, fps, graclus
from torch_scatter import scatter_add, scatter_mean


class RadiusGraph(torch.nn.Module):
    def __init__(self, r: float, self_connect: bool, max_num_neighbors: int):
        super().__init__()
        self.r: float = r
        self.self_connect: bool = self_connect
        self.max_num_neighbors: int = max_num_neighbors
        self.aggretagor = scatter_mean

    def forward(self, node_coord_src: torch.Tensor, node_feature_src: torch.Tensor, batch_src: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        assert node_coord_src.ndim == 2 and node_coord_src.shape[-1] == 3

        node_coord_dst = node_coord_src
        batch_dst = batch_src
        N_nodes = len(node_coord_dst)

        edge = radius_graph(node_coord_dst, r=self.r, batch=batch_dst, loop=self.self_connect, max_num_neighbors=self.max_num_neighbors)
        edge_dst = edge[0]
        edge_src = edge[1]
        degree = scatter_add(src = torch.ones_like(edge_dst), index = edge_dst, dim=0, dim_size=N_nodes)
        node_feature_dst = self.aggretagor(src = node_feature_src.index_select(index=edge_src, dim=0), index = edge_dst, dim=0, dim_size=N_nodes)
        
        return node_coord_dst, node_feature_dst, edge_src, edge_dst, degree, batch_dst
    
class FpsPool(torch.nn.Module):
    def __init__(self, ratio: float, random_start: bool, r: float, max_num_neighbors: int):
        super().__init__()
        self.ratio: float = ratio
        self.random_start: bool = random_start
        self.r: float = r
        self.max_num_neighbors: int = max_num_neighbors
        self.aggretagor = scatter_mean

    def forward(self, node_coord_src: torch.Tensor, node_feature_src: torch.Tensor, batch_src: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        assert node_coord_src.ndim == 2 and node_coord_src.shape[-1] == 3
        
        node_coord_dst_idx = fps(src=node_coord_src, batch=batch_src, ratio=self.ratio, random_start=self.random_start)
        node_coord_dst = node_coord_src.index_select(index=node_coord_dst_idx, dim=0)
        batch_dst = batch_src.index_select(index=node_coord_dst_idx, dim=0)
        N_nodes = len(node_coord_dst_idx)

        edge = radius(x = node_coord_src, y = node_coord_dst, r=self.r, batch_x=batch_src, batch_y=batch_dst, max_num_neighbors=self.max_num_neighbors)
        edge_dst = edge[0]
        edge_src = edge[1]
        degree = scatter_add(src = torch.ones_like(edge_dst), index = edge_dst, dim=0, dim_size=N_nodes)
        node_feature_dst = self.aggretagor(src = node_feature_src.index_select(index=edge_src, dim=0), index = edge_dst, dim=0, dim_size=N_nodes)

        return node_coord_dst, node_feature_dst, edge_src, edge_dst, degree, batch_dst