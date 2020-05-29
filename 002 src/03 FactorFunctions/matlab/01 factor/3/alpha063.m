function [X, offsetSize] = alpha063(alphaPara)
% main function
% SMA(MAX(CLOSE - DELAY(CLOSE, 1), 0), 6, 1) / SMA(ABS(CLOSE - DELAY(CLOSE,
% 1)), 6, 1) * 100
% min data size: 7
% input all the data, not just the latest 7 days' data
% alphaPara is a structure
    try
        close = alphaPara.close;
        updateFlag  = alphaPara.updateFlag;
    catch
        error 'para error';
    end

% calculate and return all history factor
% controled by updateFlag, call getAlpha if TRUE
    if ~updateFlag
        [X, offsetSize] = getAlpha(close);
        return
    else
        [X, offsetSize] = getAlphaUpdate(close);
    end
end

%-------------------------------------------------------------------------

function [exposure, offsetSize] = getAlpha(close)
% function compute alpha
    [m, n] = size(close);
    delay = [zeros(1, n);close(1: m - 1,:)];
    maxMatrix = max(close - delay, zeros(m, n));
    absMatrix = abs(close - delay);
    
    exposure = sma(maxMatrix, 6, 1)./ sma(absMatrix, 6, 1) * 100;
    offsetSize = 6;
end

function [exposure, offsetSize] = getAlphaUpdate(close)
% function compute alpha
    offsetSize = 7;
    [m, n] = size(close);
    if m < offsetSize
        error 'Lack data. At least data of 7 days.';
    end
    delay = close(m - 6: m - 1, :);
    closeTable = close(m - 5: m, :);
    maxMatrix = max(closeTable - delay, zeros(6, n));
    absMatrix = abs(closeTable - delay);
    exposure = sma(maxMatrix, 6, 1)./ sma(absMatrix, 6, 1) * 100;
    exposure = exposure(6, :);
end
