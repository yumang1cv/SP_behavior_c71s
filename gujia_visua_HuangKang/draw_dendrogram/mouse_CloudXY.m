function mouse_CloudXY(avg_skeleton, avg_coord, clus_energy, selection, temClus_aliXYZ, limHor, limVert, i_clus)

cmap_MC = jet(100);

% 0 : skeleton will not be drawn, Eg : [ 1 2; 2 3;], draws lines between features 1 and 2, 2 and 3
drawline = [ 1 2; 1 3;2 3; 4 5;4 6;5 7;6 8;7 14;8 14;...
    5 9;7 11;6 10; 8 12;14 15; 15 16];

%%
tem_clus_energy = clus_energy{1, i_clus};
energy_temX = reshape(mean(tem_clus_energy(1, selection, :), 1), length(selection), size(tem_clus_energy, 3));
energy_temY = reshape(mean(tem_clus_energy(2, selection, :), 1), length(selection), size(tem_clus_energy, 3));
energy_temZ = reshape(mean(tem_clus_energy(3, selection, :), 1), length(selection), size(tem_clus_energy, 3));

energy_temMeanX = mean(energy_temX, 2); 
energy_temMeanY = mean(energy_temY, 2); 
energy_temMeanZ = mean(energy_temZ, 2);
energy_temMeanH = energy_temMeanX + energy_temMeanY;
energy_temMeanHNM = (energy_temMeanH - limHor(1))/(limHor(2) - limHor(1));

clusPoints = [reshape(temClus_aliXYZ(1, :, :), 1, size(temClus_aliXYZ, 2)*size(temClus_aliXYZ, 3)); ...
    reshape(temClus_aliXYZ(2, :, :), 1, size(temClus_aliXYZ, 2)*size(temClus_aliXYZ, 3))];

clusCloudMat = creatEmptyMat(clusPoints', 0, 1, 1);
for ib = 1:length(selection)
    temPoints = [reshape(temClus_aliXYZ(1, selection(ib), :), 1, size(temClus_aliXYZ, 3)); ...
        reshape(temClus_aliXYZ(2, selection(ib), :), 1, size(temClus_aliXYZ, 3))];
    
    temCloudMat = estim_density(temPoints', 0, 1, 1);
    clusCloudMat = fillPDFMat(clusCloudMat, temCloudMat, energy_temMeanHNM(ib));
end

%%
tem_avg_skeleton = avg_skeleton{1, i_clus};
xmax = max(tem_avg_skeleton(1, :)) + 20; xmin = min(tem_avg_skeleton(1, :)) - 20;
ymax = max(tem_avg_skeleton(2, :)) + 15; ymin = min(tem_avg_skeleton(2, :)) - 15;
zmax = max(tem_avg_skeleton(3, :)) + 50; zmin = min(tem_avg_skeleton(3, :)) - 50;

%%
hold on
scatter3(tem_avg_skeleton(1, :), tem_avg_skeleton(2, :), tem_avg_skeleton(3, :), 6, ...
    'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'k', 'LineWidth', 0.05);
mesh_mouse_avg(avg_coord{1, i_clus}', 1)

for l = 1:size(drawline,1)
    pts = [tem_avg_skeleton(:,drawline(l,1))'; tem_avg_skeleton(:,drawline(l,2))']; %line btw elbow and shoulder
    line(pts(:,1), pts(:,2), pts(:,3),'color','k','linewidth', 0.5)
end

%%
imagesc(clusCloudMat.X, clusCloudMat.Y, clusCloudMat.PPDF);
colormap(cmap_MC);
caxis([0, 1]); view(0, 90); alpha color

set(gca, 'XTickLabel', [], 'YTickLabel', [], 'TickLength',[0, 0], 'Box', 'on')
xlim([xmin, xmax]); ylim([ymin, ymax]); zlim([zmin, zmax]);












