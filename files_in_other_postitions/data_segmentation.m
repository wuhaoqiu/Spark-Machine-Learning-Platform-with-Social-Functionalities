%% SensAI - virtual data generation script - Version 1.0b

% Scipt that generates a large volume of virtual/synthetic data for use in
% training bi-directional LSTM ANN model for exercise quality prediction

clc;
close all;
clear all;

%% load data
training_series_time=load('time.mat')
training_series_amplitude=load('amplitude.mat')
%% Curve seperation

% in this loop, each training example is processed for curve seperation
for qq=1:num_series

strain = training_series_amplitude{qq}(1,:) ;
time = training_series_time{qq}(1,:) ;
strain = strain';
time = time';
L = length(time);

% in this part, the continuos curve converts to a stepwise curve. 
% each block is a step. blocks are defined by the time intervals of 0.1 s 
int = 0.1;
n_blocks = floor( time(L) /int) ;

if rem(time(L),int)~=0
    n_blocks = n_blocks+1 ;
end

blocks = zeros(n_blocks,3) ;
%intra group numerator
k=0;
%inter group numerator
n=1;
sum = 0;
%computing average strain of each block
for i=1:L
    
    if time(i,1) > n*int
        blocks(n,1)=n;
        blocks(n,2) = 100* sum / k; 
        n=n+1;
        k=0;
        sum = 0;
    end   
    k = k+1 ;
    sum = sum+strain(i) ;
end

%last block calculations
sum = 0;
blocks(n_blocks,1)=n_blocks;
for j= (L-3):L
    sum = sum + strain(j) ;
end
blocks(n_blocks,2) = 100* sum/k ;

%strain thresholding
% syms x    
% y = piecewise(x<=20, 0, 20<x<=40, 1, 40<x<=60, 2, 60<x<=80, 3, 80<x<=100, 4,100<x<=200, 5);
for m=1:n_blocks
    if blocks(m,2)<=20
%         blocks(m,3) = subs(y, x, blocks(m,2) ) ;
        blocks(m, 3) = 0;
    elseif blocks(m,2)>20 && blocks(m,2)<=40
        blocks(m, 3) = 1;
    elseif blocks(m,2)>40 && blocks(m,2)<=60
        blocks(m, 3) = 2;
    elseif blocks(m,2)>60 && blocks(m,2)<=80
        blocks(m, 3) = 3;
    elseif blocks(m,2)>80 && blocks(m,2)<=100
        blocks(m, 3) = 4;
    else %blocks(m,2)>40 && blocks(m,2)<=60
        blocks(m, 3) = 5;
    end
end

figure
subplot(1,2,1)
plot(time,strain)
subplot(1,2,2)
plot( blocks(:,1), blocks(:,3) )


% in this part, the curves can be seperated by blocks of zero strain
Q=0;
n_curves=0;
clear divider;
for q = 1:n_blocks 
    
    %zero cells
     if blocks(q,3) == 0
         Q=Q+1 ;
     
     %the nonzero cell after a zero cell
%      else         
%          %the nonzero cell after a zero cell
     elseif blocks(q-1,3)==0

            n_curves = n_curves +1 ;
            zero_start = (q-Q-1)/10 ; % start time of zero blocks
            zero_end  = (q-1)/10 ;  % end time of zero blocks
            
            % start time of the new curve
            divider(n_curves,1)=zero_start + (zero_end - zero_start)/2 ;
            Q=0;          
  
%          end        
     end   
end

if blocks(n_blocks,3)==0
            n_curves = n_curves +1 ;
            zero_start = (q-Q)/10 ; % start time of zero blocks
            zero_end  = (q-1)/10 ;  % end time of zero blocks
            
            % start time of the new curve
            divider(n_curves,1)=(zero_end - zero_start)/2 ;
end
    
n_curves = n_curves -1 ;

%full matrix
clear full;
full = [time,strain];

%cut the curves
for p=1:n_curves

    up = divider(p+1);   %upper limit of each curve
    down = divider(p); %lower limit of each curve
    A = full(full(:,1)>down,:) ;
    A = A(A(:,1)<up,:) ;
    len = length(A(:,1));    
    FULL{p,qq} = A ;
    plot(FULL{p, qq})
    plot(FULL{p,qq}(:,1),FULL{p,qq}(:,2))
%     title('The number of strain: '+ string(qq) + ', The number of curve at this strain of data: ' + string(p))
end
end



%% Scores - for time, amplitude and shape

% Shape scores - parameterised such that for “num_curves?curve types, each with length “number_of_data? Here we assume only 3 curves types

shape_scores = zeros(num_curves*number_of_data,1);
shape_scores(1:number_of_data) = 2;
shape_scores((1+number_of_data) : 2*number_of_data) = 1;
shape_scores((1+2*number_of_data) : 3*number_of_data) = 0;


% Time scores - we must check the maximum value of time in each instance string, in order to determine the score associated with time. In general:
% time < 2.5 seconds, score = 0 (too quick)
% 2.5 < time < 4.5 seconds, score = 1
% 4.5 seconds < time, score = 0 (too slow)

time_scores = zeros(data_size,1);

for i = 1:data_size

        if max(time_matrix(i,1:string_length)) > 2.75 && max(time_matrix(i,string_length)) < 4.25
            
            time_scores(i,1) = time_scores(i,1) + 1;

        else
            
        end
end

% Amplitude scores - we must check the maximum value of normalised 
% amplitude in each instance string, in order to determine the score 
% associated with the strain. In general:
% amplitude < 0.9, score = 0 (not enough stretch)
% 0.9 < amplitude < 1.05, score = 1
% 1.05 < amplitude, score = 0 (too much stretch, possibly poor calibration)

amplitude_scores = zeros(data_size,1);

for i = 1:data_size

        if max(strain_matrix(i,1:string_length)) > 0.9 && max(strain_matrix(i,1:string_length)) < 1.05
            
            amplitude_scores(i,1) = amplitude_scores(i,1) + 1;

        else
            
        end
end

% Finally, add all of the data together to get the aggrgated scores
scores_matrix = shape_scores + time_scores + amplitude_scores;

%% Calculate first and second derivatives from data, to use as model inputs

% First derivative
diff_length = string_length - 1;
differential_data = zeros(data_size, diff_length);

for i = 1:data_size

    x_temp = time_matrix(i,:);
    y_temp = strain_matrix(i,:);
    
    dy = diff(y_temp)./ diff(x_temp);
    dy_1 = smooth(dy);
    
    differential_data(i,:) = dy_1;
    
end

% Double derivative
double_diff_length = string_length - 2;
double_differential_data = zeros(data_size, double_diff_length);

for i = 1:data_size

    x_temp1 = time_matrix(i, 1:(string_length - 1));
    y_temp1 = differential_data(i, :);
    
    ddy = diff(y_temp1)./ diff(x_temp1);
    ddy_1 = smooth(ddy);
    
    double_differential_data(i,:) = ddy_1;
      
end

%% Stitch time and strain arrays together

% Initialise the stitched matrix as array of zeros. Number of rows will be
% twice as long as data_length, as we are stitching double the data
% together
full_data_temp = zeros(3*data_size, string_length);

% Loop through and insert the necessary rows into the matrix
% number of data is 1000 here
 for i = 1:data_size
     
     full_data_temp((3*i-2),:) = strain_matrix(i,:);
     
     full_data_temp((3*i-1), 1:(string_length - 1)) = differential_data(i,:);
     
     full_data_temp((3*i), 1:(string_length - 2)) = double_differential_data(i,:);
    
 end

%% Generate Traing Data
% rowDist is 3000 * 1 vector with each vaue is 3
rowDist = zeros(data_size,1);
rowDist = rowDist + 3;
% training input is 3000*1 cell matrix
training_input = mat2cell(full_data_temp,rowDist);

