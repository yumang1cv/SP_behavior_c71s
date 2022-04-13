function decomposing_viewer3D(showVideo, showBodyFeat, showRange, mutiCam_videoPath, saveVideo_name)

% viewer of bahavior decomposition
%
% History
%   create  -  Kang Huang  (kang.huang@siat.ac.cn), 03-02-2020

writerObj = VideoWriter([saveVideo_name, '.mp4'], 'MPEG-4');
writerObj.FrameRate = 10;
writerObj.Quality = 100;
open(writerObj);

global HBT

reMap = HBT.HBT_DecData.L2.reClusData.s;
Seg = HBT.HBT_DecData.L2.reClusData;

try
    labels = G2L_Slow(Seg.G);
catch
    labels = G2L(Seg.G);
end
    
try
    label_txt = importdata('./fig4/seg1HBTGoodResults.txt');
    annotes = label_txt;
catch
    
end

CQI = evaClus_qulity();

video_names = dir([mutiCam_videoPath, '*.avi']);
video_names = {video_names.name};
vidobj1 = VideoReader([mutiCam_videoPath, video_names{1}]);
vidobj2 = VideoReader([mutiCam_videoPath, video_names{2}]);
vidobj3 = VideoReader([mutiCam_videoPath, video_names{3}]);
vidobj4 = VideoReader([mutiCam_videoPath, video_names{4}]);
HBT.DataInfo.VideoInfo1 = vidobj1;
HBT.DataInfo.VideoInfo2 = vidobj2;
HBT.DataInfo.VideoInfo3 = vidobj3;
HBT.DataInfo.VideoInfo4 = vidobj4;

rawData_names = dir([mutiCam_videoPath, '*.csv']);
rawData_names = {rawData_names.name};
[X1, Y1, ~] = readDLCRaw([mutiCam_videoPath, rawData_names{1}]);
[X2, Y2, ~] = readDLCRaw([mutiCam_videoPath, rawData_names{2}]);
[X3, Y3, ~] = readDLCRaw([mutiCam_videoPath, rawData_names{3}]);
[X4, Y4, ~] = readDLCRaw([mutiCam_videoPath, rawData_names{4}]);

% numFrames = round(vidobj.Duration.*vidobj.FrameRate);
try
    fs = HBT.DataInfo.VideoInfo.FrameRate;
catch
    fs = 30;
end
try
    cut_offset = HBT.PreproInfo.CutData.Start * fs;
catch
    cut_offset = 0;
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%
startframe = round((1/fs)*fs); endframe = 100*fs;
downsamp = 3;
ampR = 0.5;
%%%%%%%%%%%%%%%%%%%%%%%%%%%

data_len = size(HBT.RawData.X, 1);
nDim = size(HBT.RawData.X, 2);
timeLine = linspace(0, data_len/fs, data_len);
DP_sR = 1:data_len+1;


% subtract mean value of each trace
data_show = HBT.HBT_DecData.XY';
data_show = (ampR*data_show(:,:)/40 + double(1:1:size(data_show,2)))';

% get body parts names
bodyPart_name = HBT.DataInfo.Skl;

% 3D coord
coords3d = HBT.HBT_DecData.XY';
coords3d(:, 1:3:end) = HBT.RawData.X;
coords3d(:, 2:3:end) = HBT.RawData.Y;
coords3d(:, 3:3:end) = HBT.RawData.Z;
xvals = coords3d(:,1:3:nDim*3,1); 
yvals = coords3d(:,2:3:nDim*3,1);
zvals = coords3d(:,3:3:nDim*3,1);
% xmax = max(xvals(:)); xmin = min(xvals(:));
% ymax = max(yvals(:)); ymin = min(yvals(:));
xmax = 250; xmin = -250;
ymax = 250; ymin = -250;
zmax = 500; zmin = -100;

r = (xmax-xmin)/2;
[Xbox, Ybox, Zbox] = cylinder(r, 50);
Zbox = Zbox*zmax;

% panel position
pos = {[0.01 0.71 0.11 0.26], [0.125 0.71 0.11 0.26], [0.24 0.71 0.11 0.26], ...
    [0.355 0.71 0.11 0.26], [0.01 0.12 0.22 0.52], [0.245 0.12 0.22 0.52], ...
    [0.49 0.40 0.50 0.56], [0.49 0.12 0.50 0.08], [0.49 0.26 0.50 0.08]};
n_bodyParts = nDim;
%0 : skeleton will not be drawn, Eg : [ 1 2; 2 3;], draws lines between features 1 and 2, 2 and 3
drawline = [ 1 2; 1 3;2 3; 4 5;4 6;5 7;6 8;7 14;8 14;...
    5 9;7 11;6 10; 8 12;14 15; 15 16];

figure(1)
colorclass = colormap(jet); %jet is default in DLC
clrM = colorclass(ceil(linspace(1,64,n_bodyParts)),:);
clr = flipud(clrM);
close 
set(gcf, 'Position', [250, 300, 830, 300], 'color', 'k')
fontSize = 10;

% plot body traces
subplot('Position', pos{7});
hold on
for li = 1:size(data_show, 1)/3
    for lii = 1:3
        plot(timeLine, data_show((li-1)*3 + lii, :)', 'Color', clr(li, :), 'LineWidth', 1);
    end
end
set(gca, 'Color', 'none', 'YLim', [-2*ampR, size(data_show, 1)+2*ampR], ...
    'xtick',[], 'XColor', 'none', 'YColor', 'none', 'FontSize', fontSize)
plt2 = plot([0/fs 0/fs], [-2, size(data_show, 1)+2], '--w');
hold off

% plot behavior layers
subplot('Position',pos{8});
plotSegBar(HBT.HBT_DecData.L1.MedData, DP_sR, fs, startframe, endframe)
colormap(gca, clr)
set(gca, 'Color', 'none','ytick',[], 'FontSize', fontSize, 'TickDir', 'out', ...
    'TickLength',[0, 0], 'LineWidth', 0.5, 'Box', 'off', 'XColor', 'w', 'YColor', 'w')
xlabel('Time (s)')
hold on
plt3 = plot([0/fs 0/fs], [0 1], '--w');
hold off

subplot('Position',pos{9});
plotSegBar(HBT.HBT_DecData.L2.reClusData, DP_sR, fs, startframe, endframe)
colormap(gca, clr)
set(gca, 'Color', 'none', 'ytick',[], 'xtick',[], 'FontSize', fontSize, ...
    'TickDir', 'out', 'TickLength',[0, 0], 'LineWidth', 0.5, 'Box', 'off', 'XColor', 'w', 'YColor', 'w')
hold on
plt4 = plot([0/fs 0/fs], [0 1], '--w');
hold off
% axis off


% plot loop
frame1 = read(vidobj1, 1);
frame2 = read(vidobj2, 1);
frame3 = read(vidobj3, 1);
frame4 = read(vidobj4, 1);
[yl, xl, ~] = size(frame1);

tic
figure1 = figure(1);
for fi = startframe:downsamp:endframe
    
    % cam1
    subplot('Position', pos{1});
    cla
    if showVideo
        frame1 = read(vidobj1, fi+cut_offset);
        imshow(frame1)
        if showBodyFeat
            hold on
        end
    end
    
    if showBodyFeat
        for ib = 1:nDim
            plot(X1(fi, ib), Y1(fi, ib), '.', 'Color', clr(ib,:), 'MarkerSize', 5); 
        end
        set(gca,'color', 'black')
        
        if ~showVideo
            axis([0, xl, 0, yl])
            set(gca,'color', 'black', 'YDir', 'reverse')
        end
    end
    
    
    % cam2
    subplot('Position', pos{2});
    cla
    if showVideo
        frame2 = read(vidobj2, fi+cut_offset);
        imshow(frame2)
        if showBodyFeat
            hold on
        end
    end
    
    if showBodyFeat
        for ib = 1:nDim
            plot(X2(fi, ib), Y2(fi, ib), '.', 'Color', clr(ib,:), 'MarkerSize', 5); 
        end
        set(gca,'color', 'black')
        
        if ~showVideo
            axis([0, xl, 0, yl])
            set(gca,'color', 'black', 'YDir', 'reverse')
        end
    end
    
    % cam3
    subplot('Position', pos{3});
    cla
    if showVideo
        frame3 = read(vidobj3, fi+cut_offset);
        imshow(frame3)
        if showBodyFeat
            hold on
        end
    end
    
    if showBodyFeat
        for ib = 1:nDim
            plot(X3(fi, ib), Y3(fi, ib), '.', 'Color', clr(ib,:), 'MarkerSize', 5); 
        end
        set(gca,'color', 'black')
        
        if ~showVideo
            axis([0, xl, 0, yl])
            set(gca,'color', 'black', 'YDir', 'reverse')
        end
    end
    
    % cam4
    subplot('Position', pos{4});
    cla
    if showVideo
        frame4 = read(vidobj4, fi+cut_offset);
        imshow(frame4)
        if showBodyFeat
            hold on
        end
    end
    
    if showBodyFeat
        for ib = 1:nDim
            plot(X4(fi, ib), Y4(fi, ib), '.', 'Color', clr(ib,:), 'MarkerSize', 5); 
        end
        set(gca,'color', 'black')
        
        if ~showVideo
            axis([0, xl, 0, yl])
            set(gca,'color', 'black', 'YDir', 'reverse')
        end
    end
    
    h3d = subplot('Position', pos{5});
    curLabel = labels(find(fi >= reMap, 1, 'last'));
    cla
    surf(Xbox, Ybox, Zbox, 'FaceAlpha',0.1, 'EdgeColor', 'none', 'FaceColor', [.9 .9 .9]);
    hold on
    mesh_mouse(coords3d, fi)
    
    temp = reshape(coords3d(fi,:,1),3,nDim);
    scatter3(temp(1,:),temp(2,:),temp(3,:), 10*ones(1,nDim), clr(1:nDim,:),'filled','Parent', h3d);
    
    for l = 1:size(drawline,1)
        pts = [temp(:,drawline(l,1))'; temp(:,drawline(l,2))']; %line btw elbow and shoulder
        line(pts(:,1), pts(:,2), pts(:,3),'color','w','linewidth',1.5,'Parent', h3d)
    end
    
    hold off ;
    set(h3d,'Color', 'none','xlim',[xmin xmax],'ylim',[ymin ymax],'zlim',[zmin zmax], 'TickLength',[0.01, 0.01]) ;
    set(h3d,'view',[22, 48], 'xticklabel',{[]},'yticklabel',{[]},'zticklabel',{[]}, 'XColor', 'w', 'YColor', 'w', 'ZColor', 'w');
    title('3D reconstruction', 'FontSize', fontSize, 'Color', 'w');
    
    htp = subplot('Position', pos{6});
    cla
    plot(Xbox(1, :), Ybox(1, :), 'w-')
    hold on
    mesh_mouse(coords3d, fi)
    scatter3(temp(1,:),temp(2,:),temp(3,:), 10*ones(1,nDim), clr(1:nDim,:),'filled','Parent', htp);
    
    for l = 1:size(drawline,1)
        pts = [temp(:,drawline(l,1))'; temp(:,drawline(l,2))']; %line btw elbow and shoulder
        line(pts(:,1), pts(:,2), pts(:,3),'color','w','linewidth',1,'Parent', htp)
    end

    try
        plot3(coords3d(fi-60:fi, 46), coords3d(fi-60:fi, 47), coords3d(fi-60:fi, 48), ...
            'Marker', '.', 'MarkerSize', fontSize, 'Color', 'r', 'Parent', htp)
    catch
        
    end
    hold off
    set(htp,'view',[0, 90], 'xticklabel',{[]},'yticklabel',{[]},'zticklabel',{[]}, 'XColor', 'w', 'YColor', 'w');
    title([{[annotes{curLabel}, ' ', ...
        num2str(CQI(find(fi >= reMap, 1, 'last')), '%4.2f')]}, {'Top View'}], 'FontSize', fontSize, 'Color', 'w'); 
    axis equal
    set(htp,'Color', 'none','xlim',[xmin xmax],'ylim',[ymin ymax],'zlim',[zmin zmax], 'TickLength',[0.01, 0.01]) ;
    
    
    subplot('Position', pos{7});
    xlim([(fi-1)/fs+showRange(1), (fi-1)/fs+showRange(2)])
    set(plt2, 'XData', [fi/fs, fi/fs])
    
    
    subplot('Position', pos{8});
    xlim([(fi-1)/fs+showRange(1), (fi-1)/fs+showRange(2)])
    set(plt3, 'XData', [fi/fs, fi/fs])
    
    subplot('Position', pos{9});
    xlim([(fi-1)/fs+showRange(1), (fi-1)/fs+showRange(2)])
    set(plt4, 'XData', [fi/fs, fi/fs])
    title(['Current Movement: ', annotes{curLabel}, '  CQI: ', ...
        num2str(CQI(find(fi >= reMap, 1, 'last')), '%4.2f')], 'FontSize', fontSize, 'Color', 'w')

    drawnow
    toc
    f = getframe(figure1);
    writeVideo(writerObj, f.cdata);
end
disp('end')
close(writerObj);