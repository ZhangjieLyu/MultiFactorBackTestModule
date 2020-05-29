function [X, offsetSize] = HSIGMA(alphaPara)
% Returns the log value of the total market capital of single stocks
% log(total market capital)
% min data size: 1
% alphaPara is a structure
try
    close = alphaPara.close;
    indexReturn = alphaPara.indexTotalReturn;
    updateFlag  = alphaPara.updateFlag;
catch
    error 'para error';
end

% calculate and return all history factor
% controled by updateFlag, call getAlpha if TRUE
if ~updateFlag
    [X, offsetSize] = getHSIGMA(close,indexReturn);
    return
else
    [X, offsetSize] = getHSIGMAUpdate(close,indexReturn);
end
end

%-------------------------------------------------------------------------
function rts = calRts(close)
[~,n] = size(close);
closeYesterday = [zeros(1,n);close(1:end-1,:)];
rts = close ./ closeYesterday -1;
end

function [exposure, offsetSize] = getHSIGMA(close,indexReturn)
warning('off')
% function compute factor exposure of style factor
rts = calRts(close);
[m,n] = size(close);
w = ExponentialWeight(250, 60);
%beta = zeros(m,n);
exposure = zeros(m,n);
for i = 251:m %days
    disp(strcat('start process day :', int2str(i)));
    sliceRts = rts(i-250+1:i,:);
    sliceIndexReturn = indexReturn(i-250+1:i);
    sliceRts = w.*sliceRts;
    sliceIndexReturn = w.*sliceIndexReturn;
    
    for j =1:n %stocks
        BigMatrix = [sliceRts(:,j),sliceIndexReturn];
        BigMatrix = rmmissing(BigMatrix,1);
        [infRow,~] = find(isinf(BigMatrix));
        BigMatrix(infRow, :) = [];
        [~,~,residuals] = regress(BigMatrix(:,2),BigMatrix(:,1));
        thisStd = std(residuals);
        exposure(i,j) = thisStd ;
    end
end
offsetSize = 252;
end

function [exposure, offsetSize] = getHSIGMAUpdate(Close,indexReturn)
% function compute factor exposure of style factor
disp(strcat('process the last day'));
rts = calRts(Close);
w = ExponentialWeight(250, 60);
[m, n] = size(Close);
sliceRts = rts(m-250+1:m,:);
sliceIndexReturn = indexReturn(m-250+1:m);
sliceRts = w.*sliceRts;
sliceIndexReturn = w.*sliceIndexReturn;
tic
for j =1:n %stocks
    BigMatrix = [sliceRts(:,j),sliceIndexReturn];
    BigMatrix = rmmissing(BigMatrix,1);
    [infRow,~] = find(isinf(BigMatrix));
    BigMatrix(infRow, :) = [];
    [~,~,residuals] = regress(BigMatrix(:,2),BigMatrix(:,1));
    thisStd = std(residuals);
    exposure(m,j) = thisStd;
end
offsetSize = 252;
toc
end
